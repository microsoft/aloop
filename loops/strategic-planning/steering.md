# Strategic Planning & Prioritization

## Goal
Develop a feature prioritization recommendation for **[YOUR PRODUCT/ORG, e.g.,
"Contoso Platform"]** for the **[TIME PERIOD, e.g., "H2 2026"]** planning cycle,
considering market trends, customer signals, competitive landscape, and
engineering capacity.

**One-Sentence Summary**:
> [e.g., "A prioritized H2 roadmap recommendation for Azure AI Agent Platform
> that argues for 3 big bets and says no to 5 popular requests."]

## Success Criteria (in priority order)
- [ ] **One-page executive summary** — top 3 bets + rationale (NON-NEGOTIABLE, goes first)
- [ ] Market context with 5+ supporting data points
- [ ] Customer signal summary — top 10 requests, synthesized not listed
- [ ] Competitive gap analysis (vs. top 2-3 competitors)
- [ ] Feature list with RICE scoring (Reach, Impact, Confidence, Effort)
- [ ] Recommended priority stack rank with rationale
- [ ] "If we could only do 3 things" section
- [ ] Risk assessment for top 3 bets
- [ ] "Contrarian take" — what we should NOT do and why
- [ ] 2500-5000 words
- Score target: 85/100

## Constraints
- Weight customer feedback 2x over competitive parity in scoring
- Output file: artifacts/strategy.md
- Be willing to recommend cutting features — saying no is a strategy
- Use tables for RICE scoring

## Instructions to Agent
- IMPORTANT: Write the ENTIRE strategy in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with the executive summary. If the VP stops reading after page 1, they
  should still know your recommendation.
- Don't just list — synthesize and argue for a position. "We should bet on X
  because Y, even though Z is more popular" is useful. "Here are 15 things we
  could do" is not.
- DO NOT RAMBLE. Long strategy docs get skimmed. Make every paragraph earn its
  place.
- The "contrarian take" section is where the real insight lives. What's the
  popular thing everyone assumes we should do that's actually wrong?
- Write for two audiences: the executive (summary, stack rank, 3 bets) and
  the planner (RICE scores, gap analysis, risk factors).

## Loop Settings
- interval_minutes: 15
- max_iterations: 18
- abort: false
