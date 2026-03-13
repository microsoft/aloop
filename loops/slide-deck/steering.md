# Slide Deck Generator

## Goal
Create a **[NUMBER]-slide presentation**: **"[YOUR TITLE, e.g., 'The Future of
AI Agents — What Changes When They Run Overnight']"** for **[YOUR AUDIENCE,
e.g., "a conference talk (developers and PMs)"]**.

**One-Sentence Summary**:
> [e.g., "A 15-slide conference talk that convinces developers to rethink AI
> from one-shot prompts to autonomous overnight loops."]

## Success Criteria (in priority order)
- [ ] **Opening hook** — first slide after title grabs attention (NON-NEGOTIABLE)
- [ ] Clear narrative arc: problem → insight → solution → proof → call to action
- [ ] Each slide: ≤6 bullets, ≤10 words each
- [ ] Speaker notes for every slide
- [ ] "So what" test: every slide answers why the audience should care
- [ ] Diagrams where architecture or flow needs visualization (mermaid)
- [ ] Closing slide with a concrete next step the audience can take
- [ ] Output as markdown with speaker notes
- Score target: 82/100

## Constraints
- Conference-style: visual, minimal text, punchy
- Output files: artifacts/slides.md, artifacts/slides-notes.md
- Maximum [NUMBER] slides — every slide must earn its place
- No walls of text. If a bullet needs a paragraph, it's not a bullet.

## Instructions to Agent
- IMPORTANT: Write the ENTIRE deck in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- The opening hook decides whether 200 people look up from their laptops.
  Don't waste it on an agenda slide.
- DO NOT RAMBLE in speaker notes. Each note should be 2-3 sentences max — what
  to say and why this slide matters.
- Write for two audiences: the room (slides — scannable, visual) and the
  speaker (notes — what to say, when to pause, where to demo).
- Use mermaid for diagrams. If a concept is spatial or sequential, draw it.
- Kill any slide that's "nice to have." If removing it doesn't break the story,
  it shouldn't be there.

## Loop Settings
- interval_minutes: 10
- max_iterations: 15
- abort: false
