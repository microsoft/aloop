# Documentation Writer

## Goal
Write a complete documentation set for **[YOUR PRODUCT/FEATURE, e.g., "Getting
Started with Contoso SDK"]** covering quickstart through advanced configuration.

**One-Sentence Summary**:
> [e.g., "A 5-page documentation set that takes a developer from zero to
> deployed in under 10 minutes, then teaches them to customize."]

## Success Criteria (in priority order)
- [ ] **Quickstart guide** — deploy or use in <10 minutes, ≤3 commands (NON-NEGOTIABLE, goes first)
- [ ] Concepts overview — what it is, how it works, why it matters
- [ ] Tutorial — build something real, step by step
- [ ] How-to guide for the most common customization task
- [ ] Reference — configuration, environment variables, schema
- [ ] All code examples are copy-paste runnable
- [ ] Troubleshooting section for top 5 failure modes
- [ ] Cross-links between pages
- [ ] 4000-8000 words total across all pages
- Score target: 90/100

## Constraints
- Active voice, 2nd person ("you"), task-oriented
- Output files: artifacts/docs/ directory with separate files per page
- Each code block specifies the language for syntax highlighting
- Include expected output after commands where possible

## Instructions to Agent
- IMPORTANT: Write EACH doc page in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- The quickstart is the front door. If it's confusing, nothing else matters.
  Test every command in your head — does it actually work?
- Put the "what" and "why" in the concepts page, not the quickstart. The
  quickstart is pure action.
- DO NOT RAMBLE. If a paragraph doesn't help the reader complete a task, cut it.
- Write for two audiences: the skimmer (headings, code blocks, bold text) and
  the reader (explanations between them).

## Loop Settings
- interval_minutes: 12
- max_iterations: 20
- abort: false
