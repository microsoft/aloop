# Blog Writer Demo — aloop writing about itself

## Goal
Write an extremely compelling, clear, and visually engaging blog post that works
for **both developers AND non-technical readers**.

Title guidance — pick something jargon-free and concrete:
- **Good**: "How to Run Your Own AI Agent in the Cloud", "Build a Self-Improving AI Agent with Just Text"
- **Bad**: "Agentic Loop Orchestration Architecture", anything with "paradigm" or "synergy"

The post introduces aloop: an open-source azd template that deploys a single
autonomous AI agent into Azure Container Apps. The agent reads plain-text
instructions, plans, executes, self-evaluates with a 0-100 score,
keeps-or-discards each attempt, and loops — getting measurably better every
iteration, overnight, without human intervention.

The blog post IS the demo. This agent is writing and refining this very blog post
about itself. That's the hook.

**One-Sentence Summary** (include this near the top of the post):
> This guide shows how anyone can run a cloud AI agent that improves its work in a loop — configured with plain text, deployed with 3 commands.

## Success Criteria (in priority order)
- [ ] Opening hook + meta angle (this blog was written by the thing it describes)
- [ ] One-sentence summary near the top
- [ ] **"Why This Matters" section** — pain + value prop in the first 1/3 (NON-NEGOTIABLE)
- [ ] Core idea explained with analogy (junior employee who plans, tries, reviews, tries again)
- [ ] "How It Works" — numbered steps a non-coder can follow
- [ ] Comparison table: aloop vs autoresearch / Claude Code / ChatGPT
- [ ] 5+ concrete use cases — prominent, not an afterthought
- [ ] Working `azd` deploy example (3 commands)
- [ ] Score progression story (3-4 sentences — brief, not a section)
- [ ] Key takeaways (3 crisp bullets)
- [ ] Succinct — 600-900 words
- [ ] Short closing — 2 sentences max
- Score target: 92/100

## Constraints
- No marketing speak, no "revolutionary", no "game-changing"
- No cliché openings ("In today's fast-paced world…")
- Output file: artifacts/blog-post.md
- Include a metadata header with title, author, date, tags

## Instructions to Agent
- IMPORTANT: Write the ENTIRE blog post in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read_file("artifacts/blog-post.md") first. Build on what you have.
- The killer angle: this post was iteratively refined by the very agent it describes.
- Follow **Problem → Idea → Example → How to use**.
- Write for MIXED audience: developers AND non-technical readers.
- Growth mindset angle: cheap model + 25 iterations ($6-16) beats expensive single-shot ($5-15). Compound interest vs lottery ticket.
- Use short paragraphs (2-3 sentences). Numbered steps. Analogies before technical detail.
- DO NOT RAMBLE. Every paragraph must earn its place.

## Loop Settings
- interval_minutes: 10
- max_iterations: 25
- abort: false
