# Strategic Planning Demo — Azure AI Agent Platform H2 2026

## Goal
Create the **H2 2026 Feature Prioritization Plan** for a fictional "Azure AI
Agent Platform" team — the kind of strategic document that gets shared in a
leadership review and actually changes roadmap decisions.

**One-Sentence Summary**:
> A strategic planning document that uses RICE scoring, competitive analysis,
> and contrarian reasoning to prioritize the next 6 months of an AI platform.

## Success Criteria (in priority order)
- [ ] **Executive summary** — 5-sentence version a VP reads in 30 seconds (NON-NEGOTIABLE)
- [ ] Market context — 2026 AI agent landscape, key shifts, competitive threats
- [ ] Feature candidates — 8-12 features with one-sentence descriptions
- [ ] RICE scoring matrix — Reach, Impact, Confidence, Effort for each feature
- [ ] Prioritized roadmap — ordered by RICE, grouped into Must/Should/Could
- [ ] Competitive analysis table — aloop vs AutoGen vs CrewAI vs LangGraph vs custom
- [ ] Contrarian takes — 2-3 "things we should stop doing" recommendations
- [ ] Resource allocation — team size assumptions, capacity model
- [ ] Risk register — top 5 risks with mitigation strategies
- [ ] Success metrics — how we know H2 worked, leading + lagging indicators
- Score target: 85/100

## Constraints
- 2500-3500 words
- Output file: artifacts/strategy.md
- Mixed audience: VP who approves budget + PM who owns roadmap + eng lead who estimates
- Use markdown tables for RICE scoring and competitive analysis
- Every recommendation must have a "because" — no unsupported assertions

## Instructions to Agent
- IMPORTANT: Write the FULL plan in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Executive summary FIRST. If the VP stops reading after 5 sentences, they should
  still know the top 3 priorities and why.
- RICE scores must be internally consistent. If you say reach is 10K and impact
  is 3x, the math must hold.
- Contrarian takes are the most valuable section. "Stop investing in X" is harder
  to write than "invest in Y" — do the hard thing.
- Competitive analysis: be specific. "CrewAI does X better" not "competitors exist."
- DO NOT RAMBLE. Strategic docs that ramble lose credibility. Every paragraph must
  survive: "does this change a decision?"
- Risk register: real risks, not "could be late." Name the scenario and the blast radius.
- Success metrics: include at least one metric that could FAIL (honest planning).

## Loop Settings
- interval_minutes: 12
- max_iterations: 20
- abort: false
