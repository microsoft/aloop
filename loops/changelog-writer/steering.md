# Changelog & Release Notes

## Goal
Generate professional, user-facing release notes for **[YOUR PRODUCT/VERSION,
e.g., "Contoso SDK v3.0.0"]** by synthesizing changes into clear, categorized
documentation that helps users understand what changed and what to do about it.

**One-Sentence Summary**:
> [e.g., "These release notes cover everything new, improved, and fixed in
> Contoso SDK v3.0.0 — plus migration steps for breaking changes."]

## Success Criteria (in priority order)
- [ ] **Highlights section** — top 3 changes with "so what" for each (NON-NEGOTIABLE)
- [ ] Categorized: New Features, Improvements, Bug Fixes, Breaking Changes
- [ ] Each entry has a user-facing description (not commit-message style) explaining the "why"
- [ ] Breaking changes include step-by-step migration guidance
- [ ] Professional tone matching real SDK changelogs
- [ ] Succinct — 500-1500 words, no padding
- Score target: 88/100

## Constraints
- Follow Keep a Changelog format
- Output file: artifacts/release-notes.md
- No internal jargon — write for the developers using the product

## Instructions to Agent
- IMPORTANT: Write the ENTIRE release notes in a single write_file call.
- Before rewriting, ALWAYS read_file("artifacts/release-notes.md") first. Build on what you have.
- Each entry should answer "why should a user care?" not just "what changed."
- Breaking changes are the most important section — get the migration steps right.
- Use consistent formatting: feature name, one-sentence description, brief details.
- DO NOT RAMBLE. Changelogs should be scannable, not prose. Use bullet points.

## Loop Settings
- interval_minutes: 8
- max_iterations: 12
- abort: false
