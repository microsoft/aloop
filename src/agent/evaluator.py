"""Evaluator — scores output against rubric, provides critique."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from planner import IterationPlan
from steering import SteeringDoc

logger = logging.getLogger("aloop")

EVALUATOR_SYSTEM_PROMPT = """You are the EVALUATOR module of an autonomous agent loop.

Your job: score the agent's output HONESTLY against the evaluation rubric.
You must be critical — inflated scores waste iterations.

Output valid JSON:
{
  "score": 0-100,
  "breakdown": [
    {"criterion": "name", "score": 0-10, "max": 10, "comment": "why"}
  ],
  "overall_critique": "What's good and what's missing",
  "self_critique": "Most important thing to improve next iteration",
  "suggestions": ["suggestion1", "suggestion2"],
  "completion_assessment": "How close is this to the target goal"
}

Scoring guidelines:
- 0-20: Barely started, major gaps
- 20-40: Foundation laid but incomplete
- 40-60: Roughly half done, visible progress
- 60-80: Good work, needs refinement
- 80-90: Strong, minor improvements needed
- 90-100: Excellent, meets or exceeds all criteria

Be honest. A score of 50 is FINE for early iterations. The agent improves over time.
Do NOT inflate scores to seem positive. The agent relies on accurate scores to improve.
"""


@dataclass
class Evaluation:
    score: int = 0
    breakdown: list[dict] = field(default_factory=list)
    overall_critique: str = ""
    self_critique: str = ""
    suggestions: list[str] = field(default_factory=list)
    completion_assessment: str = ""
    raw_json: dict = field(default_factory=dict)


def evaluate_output(
    call_model_fn,
    plan: IterationPlan,
    steering: SteeringDoc,
    execution_summary: str,
    artifacts_listing: str,
    artifact_samples: str,
    primary_artifact: str = "",
) -> Evaluation:
    """Evaluate the agent's output against the rubric."""

    rubric_text = "\n".join(
        f"- {r.get('criterion', '?')} (weight: {r.get('weight', 5)}): "
        f"{r.get('description', '')}"
        for r in plan.evaluation_rubric
    )

    criteria_text = "\n".join(f"- {c}" for c in steering.success_criteria)

    # Build the artifact section — primary artifact in full, others as samples
    artifact_section = ""
    if primary_artifact:
        artifact_section = f"""## Primary Artifact (artifacts/blog-post.md) — FULL CONTENT
{primary_artifact[:50000]}"""
    if artifact_samples:
        artifact_section += f"""\n\n## Other Artifacts (samples)
{artifact_samples[:5000]}"""

    prompt = f"""## Goal
{steering.goal}

## Success Criteria (from steering.md)
{criteria_text}

## Evaluation Rubric (from planner)
{rubric_text}

## What the Executor Did
{execution_summary[:3000]}

## Files in Workspace
{artifacts_listing}

{artifact_section}

Score this output against the FULL artifact content above. You can see the entire document.
Be honest and critical."""

    raw_response = call_model_fn(
        instructions=EVALUATOR_SYSTEM_PROMPT,
        prompt=prompt,
    )

    return _parse_evaluation(raw_response)


def _parse_evaluation(raw: str) -> Evaluation:
    """Parse evaluation JSON from model response."""
    ev = Evaluation()

    text = raw.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    try:
        data = json.loads(text)
        ev.score = int(data.get("score", 0))
        ev.breakdown = data.get("breakdown", [])
        ev.overall_critique = data.get("overall_critique", "")
        ev.self_critique = data.get("self_critique", "")
        ev.suggestions = data.get("suggestions", [])
        ev.completion_assessment = data.get("completion_assessment", "")
        ev.raw_json = data
    except (json.JSONDecodeError, ValueError):
        logger.warning("Failed to parse evaluation JSON")
        # Try to extract just the score
        import re
        score_match = re.search(r'"score"\s*:\s*(\d+)', raw)
        if score_match:
            ev.score = int(score_match.group(1))
        ev.overall_critique = raw[:500]

    # Clamp score
    ev.score = max(0, min(100, ev.score))
    return ev
