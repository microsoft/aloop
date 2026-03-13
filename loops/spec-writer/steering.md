# Product Spec Writer

## Goal
Write a product specification for **[YOUR PRODUCT/FEATURE, e.g., "Contoso
Autonomous Agent Hosting"]** — covering the problem, proposed solution,
developer experience, and open questions.

**One-Sentence Summary**:
> [e.g., "A spec for managed autonomous agent hosting on Azure, aimed at getting
> engineering and PM alignment before we write a line of code."]

## Success Criteria (in priority order)
- [ ] **Problem statement** with 3 customer scenarios ("As a ___, I want to...") (NON-NEGOTIABLE, goes first)
- [ ] Proposed solution with architecture diagram (mermaid)
- [ ] Developer experience walkthrough — deploy, configure, monitor
- [ ] Non-goals clearly stated — what this is NOT
- [ ] Security model (auth, access control, network)
- [ ] Open questions section with at least 5 items
- [ ] Success metrics — how do we know this worked?
- [ ] "Day in the life" scenario for a target user
- [ ] 2000-4000 words
- Score target: 88/100

## Constraints
- Target audience: engineering team + partner PMs
- Output file: artifacts/product-spec.md
- Be specific about what's new vs. what already exists
- Include cost/pricing considerations

## Instructions to Agent
- IMPORTANT: Write the ENTIRE spec in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with the problem, not the solution. If the reader doesn't feel the pain
  by paragraph 3, the spec has failed.
- The non-goals section is as important as the goals. It prevents scope creep
  and shows you've thought about boundaries.
- DO NOT RAMBLE. Every section should earn its place. If removing a section
  doesn't weaken the argument, remove it.
- Open questions should be genuine — things you actually don't know, not
  rhetorical questions. Each should name who needs to answer it.
- Write for two audiences: the skimmer (executive summary, diagrams, bold
  decisions) and the builder (technical details, trade-offs, constraints).

## Loop Settings
- interval_minutes: 12
- max_iterations: 20
- abort: false
