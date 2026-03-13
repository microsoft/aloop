# Deep Research Demo — The Importance of Anthropic's Messages API

## Goal
Produce a comprehensive research report analyzing why Anthropic's Messages
API and SDK design has become influential in the AI SDK landscape. Compare
it against the OpenAI API/SDK, Azure AI SDKs, Google Gemini SDK, and other
popular alternatives. Assess what Anthropic got right, what others can learn,
and where it falls short.

**One-Sentence Summary**:
> This report examines why Anthropic's Messages API design has shaped how
> developers think about AI SDKs — and what OpenAI, Azure, and others should
> steal, skip, or improve upon.

## Success Criteria (in priority order)
- [ ] **Executive summary** — findings + key takeaways in 1 page (NON-NEGOTIABLE, goes first)
- [ ] API design philosophy comparison: Anthropic Messages vs OpenAI Chat Completions vs Azure AI Inference
- [ ] Concrete code comparisons for: basic chat, streaming, tool use, multi-turn, vision
- [ ] What Anthropic got right: developer ergonomics, type safety, error design, streaming UX
- [ ] What Anthropic got wrong or is missing: ecosystem gaps, enterprise features, Azure integration
- [ ] Impact analysis: how Anthropic's patterns influenced OpenAI's Responses API and others
- [ ] Strengths/weaknesses comparison matrix across 4+ SDKs
- [ ] Clear, opinionated recommendations for SDK teams at each provider
- [ ] Sources cited with links
- [ ] 3000-6000 words
- Score target: 90/100

## Constraints
- Use only publicly available information (up to March 2026)
- Be opinionated — don't just list features, make recommendations
- Output file: artifacts/competitive-research.md
- Focus on API/SDK design quality, not model quality or benchmarks

## Instructions to Agent
- IMPORTANT: Write the ENTIRE report in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with the executive summary. Busy readers stop after page 1 — make it count.
- Compare the actual developer experience: imports, client setup, type hints, error messages.
- Show real code side-by-side — same task in Anthropic vs OpenAI vs Azure.
- Analyze how Anthropic's structured content blocks influenced the industry.
- Cover the streaming story: SSE patterns, token-by-token UX, error recovery.
- Assess tool_use design vs OpenAI function calling vs Azure extensions.
- Note enterprise gaps honestly — auth, compliance, regional availability.
- DO NOT RAMBLE. Cut any analysis that doesn't lead to a recommendation.

## Loop Settings
- interval_minutes: 12
- max_iterations: 20
- abort: false
