# SDK / API Review

## Goal
Review **[YOUR SDK OR API, e.g., "Azure AI Agent Service SDK (Python)"]** and
produce a developer experience assessment with specific, actionable feedback.

**One-Sentence Summary**:
> [e.g., "A brutally honest DX review of the Azure AI Agent Service Python SDK
> with prioritized recommendations the team can act on this sprint."]

## Success Criteria (in priority order)
- [ ] **Top 10 prioritized recommendations** — specific and actionable (NON-NEGOTIABLE, goes first)
- [ ] "First 5 minutes" experience assessment — install, import, hello world
- [ ] API surface inventory — key classes, methods, patterns
- [ ] Code examples for 3 common scenarios
- [ ] Error handling and debugging experience assessment
- [ ] Documentation quality assessment
- [ ] Missing features or gaps
- [ ] Side-by-side comparison with a competitor if relevant
- [ ] 2000-4000 words
- Score target: 85/100

## Constraints
- Be brutally honest — this is internal feedback, not marketing
- Output file: artifacts/sdk-review.md
- Use publicly available docs and packages
- Every criticism must include a specific fix suggestion

## Instructions to Agent
- IMPORTANT: Write the ENTIRE review in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with the recommendations. The team wants to know what to fix, not read
  a preamble about why DX matters.
- Try to actually use the SDK — install it, import it, write real code. Don't
  just read the docs and speculate.
- Focus on what a new developer would struggle with in the first hour.
- DO NOT RAMBLE. "The error message is unhelpful" is useless. "The error says
  'Invalid request' but should say 'Missing required field: model_id'" is useful.
- Name names — cite specific classes, methods, error messages.

## Loop Settings
- interval_minutes: 12
- max_iterations: 18
- abort: false
