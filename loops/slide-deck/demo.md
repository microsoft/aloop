# Slide Deck Demo — The Autonomous Agent Loop

## Goal
Create a 15-slide presentation: **"The Autonomous Agent Loop — Ship AI That
Improves While You Sleep"** for a conference talk audience (developers and PMs).

**One-Sentence Summary**:
> A 15-slide conference talk that convinces developers to rethink AI from
> one-shot prompts to autonomous overnight loops — with a live demo hook.

## Success Criteria (in priority order)
- [ ] **Opening hook** — "This talk was prepared by the thing I'm describing" (NON-NEGOTIABLE)
- [ ] Title slide + agenda
- [ ] "The Problem" — why one-shot AI isn't enough (2 slides)
- [ ] "The Loop" — plan/execute/evaluate/gate pattern (3 slides)
- [ ] "The Architecture" — ACA + Azure OpenAI + Blob (2 slides)
- [ ] "Demo" — steering.md walkthrough + score progression (3 slides)
- [ ] "Use Cases" — 5 real scenarios (2 slides)
- [ ] "Try It" — 3-command deploy + GitHub link (1 slide)
- [ ] Each slide: ≤6 bullets, ≤10 words each
- [ ] Speaker notes for every slide
- [ ] Mermaid diagrams for architecture/flow
- Score target: 82/100

## Constraints
- Conference-style: visual, minimal text, punchy
- 15 slides maximum — every slide must earn its place
- Output files: artifacts/slides.md, artifacts/slides-notes.md
- No walls of text

## Instructions to Agent
- IMPORTANT: Write the ENTIRE deck in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- The opening hook decides whether 200 people look up from their laptops.
  Lead with: "This talk was prepared by the thing I'm describing."
- "So what" test: every slide must answer why the audience should care.
- Include a live score counter concept in the slides.
- Make the demo section feel real, not hypothetical.
- DO NOT RAMBLE in speaker notes — 2-3 sentences max per slide.
- Kill any slide that doesn't break the story if removed.
- Use mermaid for diagrams. If a concept is spatial or sequential, draw it.

## Loop Settings
- interval_minutes: 10
- max_iterations: 15
- abort: false
