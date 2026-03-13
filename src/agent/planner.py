"""Planner — converts goal + history into a measurable action plan."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

from steering import SteeringDoc

logger = logging.getLogger("aloop")

PLAN_SYSTEM_PROMPT = """You are the PLANNER module of an autonomous agent loop.

Your job: given a goal (from steering.md) and a history of past iterations,
produce a concrete, measurable action plan for the NEXT iteration.

You must output valid JSON with this schema:
{
  "measurable_goal": "One sentence — what success looks like this iteration",
  "evaluation_rubric": [
    {"criterion": "name", "weight": 1-10, "description": "what to check"}
  ],
  "action_plan": ["step1", "step2", ...],
  "hypothesis": "Why this plan will improve the score",
  "focus_areas": ["area1", "area2"]
}

Rules:
- Be SPECIFIC. Not "improve the document" but "add competitive comparison table with 5 dimensions".
- Look at past iteration critiques and address them directly.
- If this is the first iteration, focus on building a solid foundation.
- If score is already high (>80), focus on polish and gap-filling.
- Always include at least one verification step in the plan.
"""


@dataclass
class IterationPlan:
    measurable_goal: str = ""
    evaluation_rubric: list[dict] = field(default_factory=list)
    action_plan: list[str] = field(default_factory=list)
    hypothesis: str = ""
    focus_areas: list[str] = field(default_factory=list)
    raw_json: dict = field(default_factory=dict)


def create_plan(
    call_model_fn,
    steering: SteeringDoc,
    iteration_history: list[dict],
    current_best_score: int,
    iteration_number: int,
) -> IterationPlan:
    """Create an action plan for the next iteration."""

    history_summary = _summarize_history(iteration_history)

    prompt = f"""## Current State
- Iteration: {iteration_number}
- Current best score: {current_best_score}/100
- Target score: {steering.target_score}/100

## Goal (from steering.md)
{steering.goal}

## Success Criteria
{chr(10).join(f'- {c}' for c in steering.success_criteria)}

## Constraints
{chr(10).join(f'- {c}' for c in steering.constraints)}

## Human Instructions (latest from steering.md)
{chr(10).join(f'- {i}' for i in steering.instructions)}

## Past Iteration History
{history_summary}

Produce your JSON action plan for iteration {iteration_number}."""

    raw_response = call_model_fn(
        instructions=PLAN_SYSTEM_PROMPT,
        prompt=prompt,
    )

    return _parse_plan(raw_response)


def _summarize_history(history: list[dict]) -> str:
    if not history:
        return "No prior iterations. This is the first run."

    lines = []
    for entry in history[-10:]:  # Last 10 iterations
        lines.append(
            f"- Iteration {entry.get('iteration', '?')}: "
            f"score={entry.get('score', '?')}, "
            f"kept={entry.get('kept', '?')}, "
            f"critique: {entry.get('self_critique', 'n/a')[:200]}"
        )
    return "\n".join(lines)


def _parse_plan(raw: str) -> IterationPlan:
    """Parse JSON from model response, handling markdown code fences."""
    plan = IterationPlan()

    # Try to extract JSON from the response
    text = raw.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    try:
        data = json.loads(text)
        plan.measurable_goal = data.get("measurable_goal", "")
        plan.evaluation_rubric = data.get("evaluation_rubric", [])
        plan.action_plan = data.get("action_plan", [])
        plan.hypothesis = data.get("hypothesis", "")
        plan.focus_areas = data.get("focus_areas", [])
        plan.raw_json = data
    except json.JSONDecodeError:
        logger.warning("Failed to parse plan JSON, using raw text as goal")
        plan.measurable_goal = raw[:500]
        plan.action_plan = ["Execute the goal as described"]

    return plan
