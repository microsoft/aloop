# Blog Writer

## Goal
Write an extremely compelling, clear, and accessible blog post about
**[YOUR TOPIC]** for **[YOUR AUDIENCE, e.g., "developers who've used ChatGPT
but haven't built agents"]**.

**One-Sentence Summary** (the agent will include this near the top):
> [Write one plain-language sentence that captures what the reader will learn.]

## Success Criteria (in priority order)
- [ ] Opening hook that starts with a real problem or relatable scenario
- [ ] One-sentence summary near the top — plain-language value prop
- [ ] **"Why This Matters" section** — pain point + value prop in the first 1/3 (NON-NEGOTIABLE)
- [ ] Clear explanation of the core idea using an analogy
- [ ] "How It Works" — numbered steps a non-coder can follow
- [ ] 5+ concrete use cases or examples — prominent, not an afterthought
- [ ] Succinct — 600-900 words, no repetition, every paragraph earns its place
- [ ] Tone: conversational, confident, zero fluff or marketing speak
- [ ] Key takeaways section (3 crisp bullets)
- [ ] Short closing — 2 sentences max
- Score target: 90/100

## Constraints
- No marketing speak, no "revolutionary", no "game-changing", no "paradigm shift"
- No cliché openings ("In today's fast-paced world…")
- Output file: artifacts/blog-post.md
- Include a metadata header with title, author, date, tags

## Instructions to Agent
- IMPORTANT: Write the ENTIRE blog post in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read_file("artifacts/blog-post.md") first. Build on what you have.
- Follow the **Problem → Idea → Example → How to use** pattern.
- Write for a MIXED audience: developers AND non-technical readers.
- Use short paragraphs (2-3 sentences max). Use numbered steps. Show examples.
- Explain concepts with analogies before technical detail.
- DO NOT RAMBLE. If a paragraph circles back to something already said, delete it.
- Every paragraph must earn its place. If removing a sentence doesn't change the meaning, remove it.
- Avoid jargon in titles and headings.

## Loop Settings
- interval_minutes: 10
- max_iterations: 20
- abort: false
