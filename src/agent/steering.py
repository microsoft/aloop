"""Steering document parser — reads and parses steering.md."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class SteeringDoc:
    """Parsed representation of steering.md."""

    goal: str = ""
    success_criteria: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    instructions: list[str] = field(default_factory=list)
    interval_minutes: int = 10
    max_iterations: int = 50
    target_score: int = 90
    abort: bool = False
    raw: str = ""


def parse_steering(content: str) -> SteeringDoc:
    """Parse a steering.md file into structured data."""
    doc = SteeringDoc(raw=content)

    sections: dict[str, str] = {}
    current_section = ""
    current_lines: list[str] = []

    for line in content.split("\n"):
        header_match = re.match(r"^##\s+(.+)$", line)
        if header_match:
            if current_section:
                sections[current_section.lower().strip()] = "\n".join(
                    current_lines
                ).strip()
            current_section = header_match.group(1)
            current_lines = []
        else:
            current_lines.append(line)

    if current_section:
        sections[current_section.lower().strip()] = "\n".join(
            current_lines
        ).strip()

    # Extract goal
    doc.goal = sections.get("goal", "")

    # Extract success criteria as list items
    criteria_text = sections.get("success criteria", "")
    doc.success_criteria = _extract_list_items(criteria_text)

    # Extract constraints
    constraints_text = sections.get("constraints", "")
    doc.constraints = _extract_list_items(constraints_text)

    # Extract instructions to agent
    for key in ["instructions to agent", "instructions"]:
        if key in sections:
            doc.instructions = _extract_list_items(sections[key])
            break

    # Extract loop settings
    settings_text = sections.get("loop settings", "")
    if settings_text:
        interval = re.search(r"interval_minutes:\s*(\d+)", settings_text)
        if interval:
            doc.interval_minutes = int(interval.group(1))

        max_iter = re.search(r"max_iterations:\s*(\d+)", settings_text)
        if max_iter:
            doc.max_iterations = int(max_iter.group(1))

        abort = re.search(r"abort:\s*(true|false)", settings_text, re.IGNORECASE)
        if abort:
            doc.abort = abort.group(1).lower() == "true"

    # Extract target score from criteria or settings
    score_match = re.search(
        r"[Ss]core\s*target:\s*(\d+)", content
    )
    if score_match:
        doc.target_score = int(score_match.group(1))

    # Check for abort anywhere in document
    if re.search(r"^abort:\s*true", content, re.MULTILINE | re.IGNORECASE):
        doc.abort = True

    return doc


def _extract_list_items(text: str) -> list[str]:
    """Extract markdown list items from text."""
    items = []
    for line in text.split("\n"):
        match = re.match(r"^\s*[-*]\s*(\[.\])?\s*(.+)$", line)
        if match:
            items.append(match.group(2).strip())
    return items
