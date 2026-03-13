# Deep Research

## Goal
Produce a comprehensive research report on **[YOUR TOPIC, e.g., "the state of
AI agent frameworks in 2026"]**. Compare key players across architecture,
developer experience, ecosystem maturity, and production readiness.

**One-Sentence Summary**:
> [e.g., "This report compares 6 AI agent frameworks to help your team pick the
> right one based on your stack, team size, and production requirements."]

## Success Criteria (in priority order)
- [ ] **Executive summary** — findings + recommendation in 1 page (NON-NEGOTIABLE, goes first)
- [ ] All key players covered with consistent comparison dimensions
- [ ] Architecture patterns described for each
- [ ] Code snippets demonstrating a simple example in each
- [ ] Strengths/weaknesses comparison matrix
- [ ] Clear, opinionated recommendations for specific scenarios
- [ ] "Which should I use?" decision tree
- [ ] Sources cited with links
- [ ] 3000-6000 words
- Score target: 90/100

## Constraints
- Use only publicly available information
- Be opinionated — don't just list features, make recommendations
- Output file: artifacts/research-report.md

## Instructions to Agent
- IMPORTANT: Write the ENTIRE report in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with the executive summary. Busy readers stop after page 1 — make it count.
- Be opinionated throughout. "Framework X is the best choice for Y because Z"
  is useful. "Framework X has several features" is not.
- Include a decision tree or flowchart: "If you need X, use Y. If you need Z, use W."
- Every comparison dimension needs a winner. Don't hedge everything.
- DO NOT RAMBLE. Long doesn't mean thorough. Cut any analysis that doesn't
  lead to a recommendation.

## Loop Settings
- interval_minutes: 12
- max_iterations: 20
- abort: false
