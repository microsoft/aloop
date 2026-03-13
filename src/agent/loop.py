"""aloop — the main autonomous agent loop.

Inspired by:
- Claude Code's agentic loop (gather context → take action → verify results)
- Ralph Loop (self-referential iteration until completion)
- Karpathy's autoresearch (fixed-budget experiments, keep-or-discard gating)
"""

from __future__ import annotations

import json
import logging
import sys
import time
from datetime import datetime, timezone
from functools import partial

from config import Config
from evaluator import evaluate_output
from executor import execute_plan
from model_client import call_model, create_client
from planner import create_plan
from steering import SteeringDoc, parse_steering
from storage import Storage
from tools import init_tools

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("aloop")


def main() -> None:
    """Entry point — run the autonomous agent loop."""
    logger.info("=" * 60)
    logger.info(f"  aloop starting — {Config.AGENT_NAME}")
    logger.info(f"  Model: {Config.AZURE_OPENAI_DEPLOYMENT}")
    logger.info(f"  Mode: {'LOCAL' if Config.LOCAL_MODE else 'AZURE'}")
    logger.info("=" * 60)

    # Validate config
    errors = Config.validate()
    if errors:
        for e in errors:
            logger.error(f"Config error: {e}")
        sys.exit(1)

    # Initialize
    storage = Storage()
    init_tools(storage)
    client = create_client()

    # Create bound model call functions
    call_model_simple = partial(call_model, client)
    call_model_with_tools = partial(call_model, client)

    # Load or initialize progress
    progress = _load_progress(storage)
    iteration = progress.get("total_iterations", 0)
    best_score = progress.get("best_score", 0)

    logger.info(f"Resuming from iteration {iteration}, best score: {best_score}")

    # ==================== THE LOOP ====================
    while True:
        iteration += 1
        loop_start = datetime.now(timezone.utc)

        logger.info("")
        logger.info("=" * 60)
        logger.info(f"  ITERATION {iteration}")
        logger.info("=" * 60)

        try:  # Wrap entire iteration so transient failures don't crash the agent

            # ── Phase 0: Read steering.md (fresh every iteration) ──
            logger.info("[PHASE 0] Reading steering.md...")
            steering_raw = storage.read("steering.md")
            if not steering_raw:
                logger.error("No steering.md found! Upload one to get started.")
                logger.info("Waiting 60s then retrying...")
                time.sleep(60)
                continue

            steering = parse_steering(steering_raw)

            # Check for abort
            if steering.abort:
                logger.info("ABORT signal detected in steering.md. Shutting down.")
                progress["status"] = "ABORTED"
                _save_progress(storage, progress)
                break

            # Check iteration limit
            max_iter = steering.max_iterations or Config.DEFAULT_MAX_ITERATIONS
            if iteration > max_iter:
                logger.info(f"Max iterations ({max_iter}) reached. Stopping.")
                progress["status"] = "MAX_ITERATIONS_REACHED"
                _save_progress(storage, progress)
                break

            # ── Phase 1: PLAN ──
            logger.info("[PHASE 1] Planning...")
            history = _load_iteration_log(storage)

            plan = create_plan(
                call_model_fn=call_model_simple,
                steering=steering,
                iteration_history=history,
                current_best_score=best_score,
                iteration_number=iteration,
            )
            logger.info(f"  Goal: {plan.measurable_goal[:120]}")
            logger.info(f"  Steps: {len(plan.action_plan)}")

            # ── Phase 2: EXECUTE ──
            logger.info("[PHASE 2] Executing plan...")

            # Feed the current best artifact so the executor can improve it
            # instead of rewriting from scratch each iteration
            best_artifact_content = storage.read("artifacts/blog-post.md") or ""

            execution_summary = execute_plan(
                call_model_with_tools_fn=call_model_with_tools,
                plan=plan,
                steering=steering,
                iteration_number=iteration,
                current_artifact=best_artifact_content,
            )
            logger.info(f"  Execution complete ({len(execution_summary)} chars)")

            # ── Phase 3: EVALUATE ──
            logger.info("[PHASE 3] Evaluating output...")

            # Gather artifact info for evaluation
            all_files = storage.list_files("artifacts/")
            artifacts_listing = "\n".join(all_files[:50])

            # Read the primary artifact in full for evaluation
            primary_artifact = storage.read("artifacts/blog-post.md") or ""

            # Read secondary artifacts (truncated)
            artifact_samples = ""
            for f in all_files[:5]:
                if f == "artifacts/blog-post.md":
                    continue  # Already read in full above
                content = storage.read(f)
                if content:
                    artifact_samples += f"\n--- {f} ---\n{content[:5000]}\n"

            evaluation = evaluate_output(
                call_model_fn=call_model_simple,
                plan=plan,
                steering=steering,
                execution_summary=execution_summary,
                artifacts_listing=artifacts_listing,
                artifact_samples=artifact_samples,
                primary_artifact=primary_artifact,
            )

            logger.info(f"  Score: {evaluation.score}/100 (best: {best_score})")
            logger.info(f"  Critique: {evaluation.self_critique[:150]}")

            # ── Phase 4: GATE (keep or discard) ──
            # Strict improvement only — equal scores don't replace, preventing sideways drift
            kept = evaluation.score > best_score
            if kept:
                logger.info(f"  [KEPT] Score improved: {best_score} → {evaluation.score}")
                best_score = evaluation.score
            else:
                logger.info(
                    f"  [DISCARDED] Score {evaluation.score} < best {best_score}. "
                    f"Learning from failure."
                )

            # ── Phase 5: LOG ──
            log_entry = {
                "iteration": iteration,
                "timestamp": loop_start.isoformat(),
                "plan_summary": plan.measurable_goal,
                "action_steps": len(plan.action_plan),
                "score": evaluation.score,
                "previous_best": best_score if not kept else best_score,
                "delta": evaluation.score - (best_score if not kept else (best_score - (evaluation.score - best_score) if kept else best_score)),
                "kept": kept,
                "self_critique": evaluation.self_critique,
                "suggestions": evaluation.suggestions,
                "overall_critique": evaluation.overall_critique[:500],
            }

            # Append to iteration log
            storage.append("iteration_log.jsonl", json.dumps(log_entry) + "\n")

            # Write iteration report
            report = _format_iteration_report(iteration, plan, evaluation, kept, best_score)
            storage.write(f"reports/iteration_{iteration:03d}.md", report)
            storage.write("reports/latest.md", report)

            # Update progress
            scores = progress.get("scores", [])
            scores.append(evaluation.score)
            progress = {
                "scores": scores,
                "best_score": best_score,
                "best_iteration": iteration if kept else progress.get("best_iteration", 0),
                "total_iterations": iteration,
                "status": "RUNNING",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "goal": steering.goal[:200],
            }

            # Check if target reached
            target = steering.target_score or Config.DEFAULT_TARGET_SCORE
            if best_score >= target:
                logger.info(f"TARGET REACHED! Score {best_score} >= target {target}")
                progress["status"] = "GOAL_ACHIEVED"
                _save_progress(storage, progress)

                # Write completion report
                storage.write(
                    "reports/COMPLETED.md",
                    f"# Goal Achieved!\n\n"
                    f"**Score:** {best_score}/100\n"
                    f"**Iterations:** {iteration}\n"
                    f"**Goal:** {steering.goal}\n\n"
                    f"## Final Evaluation\n{evaluation.overall_critique}\n",
                )
                logger.info("Agent loop complete. Exiting.")
                break

            _save_progress(storage, progress)

            # ── Phase 6: SLEEP ──
            interval = steering.interval_minutes or Config.DEFAULT_INTERVAL_MINUTES
            logger.info(f"Sleeping {interval} minutes before next iteration...")
            time.sleep(interval * 60)

        except Exception as exc:  # noqa: BLE001
            logger.error(f"Iteration {iteration} failed: {exc}", exc_info=True)
            logger.info("Sleeping 60s then retrying next iteration...")
            time.sleep(60)

    logger.info("aloop finished.")


def _load_progress(storage: Storage) -> dict:
    default = {"scores": [], "best_score": 0, "total_iterations": 0, "status": "NEW"}
    try:
        data = storage.read_json("progress.json")
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"Corrupt progress.json, resetting to defaults: {e}")
        storage.write_json("progress.json", default)
        return default
    if isinstance(data, dict):
        return data
    return default


def _save_progress(storage: Storage, progress: dict) -> None:
    storage.write_json("progress.json", progress)


def _load_iteration_log(storage: Storage) -> list[dict]:
    raw = storage.read("iteration_log.jsonl")
    if not raw:
        return []
    entries = []
    for line in raw.strip().split("\n"):
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def _format_iteration_report(
    iteration: int,
    plan,
    evaluation,
    kept: bool,
    best_score: int,
) -> str:
    status = "KEPT" if kept else "DISCARDED"
    breakdown_text = ""
    for item in evaluation.breakdown:
        breakdown_text += (
            f"| {item.get('criterion', '?')} "
            f"| {item.get('score', '?')}/{item.get('max', 10)} "
            f"| {item.get('comment', '')} |\n"
        )

    return f"""# Iteration {iteration} Report

**Score:** {evaluation.score}/100 | **Status:** {status} | **Best:** {best_score}/100

## Plan
{plan.measurable_goal}

### Steps
{chr(10).join(f'{i+1}. {s}' for i, s in enumerate(plan.action_plan))}

### Hypothesis
{plan.hypothesis}

## Evaluation

### Score Breakdown
| Criterion | Score | Comment |
|-----------|-------|---------|
{breakdown_text}

### Critique
{evaluation.overall_critique}

### What to Improve Next
{evaluation.self_critique}

### Suggestions
{chr(10).join(f'- {s}' for s in evaluation.suggestions)}

---
*Generated by aloop at {datetime.now(timezone.utc).isoformat()}*
"""


if __name__ == "__main__":
    main()
