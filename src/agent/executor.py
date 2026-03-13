"""Executor — runs the plan using model + tools."""

from __future__ import annotations

import logging
from typing import Callable

from planner import IterationPlan
from steering import SteeringDoc
from tools import TOOL_DEFINITIONS, execute_tool

logger = logging.getLogger("aloop")

EXECUTOR_SYSTEM_PROMPT = """You are the EXECUTOR module of an autonomous agent loop.

You have been given a plan. Your job is to EXECUTE it by using the tools available
to you. You work autonomously — make decisions, call tools, and produce artifacts.

Key behaviors:
- Follow the action plan step by step
- Use tools to read existing work, search the web, write files, run code
- If a step fails, try an alternative approach
- Write your final artifacts to files using write_file
- Be thorough — the evaluator will score your output against a rubric
- If you are producing a document, write the COMPLETE document, not a summary
- Your output files should be polished and ready for human review

When done, summarize what you accomplished and what files you created/modified.
"""


def execute_plan(
    call_model_with_tools_fn: Callable,
    plan: IterationPlan,
    steering: SteeringDoc,
    iteration_number: int,
    current_artifact: str = "",
) -> str:
    """Execute the plan using the model with tools. Returns execution summary."""

    tool_defs = TOOL_DEFINITIONS

    # Build current artifact context so the executor can improve iteratively
    artifact_section = ""
    if current_artifact:
        artifact_section = f"""\n## Current Best Artifact (improve this — do NOT start from scratch)
The content below is the current highest-scoring version. Read it carefully,
identify what the evaluator critique says is missing, and produce an improved
version that keeps everything good and adds what's missing.

```
{current_artifact[:30000]}
```\n"""

    prompt = f"""## Your Mission (Iteration {iteration_number})
{plan.measurable_goal}

## Action Plan
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(plan.action_plan))}

## Hypothesis
{plan.hypothesis}

## Focus Areas
{chr(10).join(f'- {area}' for area in plan.focus_areas)}

## Goal Context
{steering.goal}

## Constraints
{chr(10).join(f'- {c}' for c in steering.constraints)}

## Human Instructions
{chr(10).join(f'- {i}' for i in steering.instructions)}
{artifact_section}
Execute this plan now. Use tools to read existing work, research, and write improved artifacts.
Start by checking what files already exist with list_files, then proceed with the plan."""

    result = call_model_with_tools_fn(
        instructions=EXECUTOR_SYSTEM_PROMPT,
        prompt=prompt,
        tools=tool_defs,
        tool_executor=execute_tool,
    )

    return result
