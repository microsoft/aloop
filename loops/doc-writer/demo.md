# Documentation Writer Demo — Getting Started with aloop

## Goal
Write a complete "Getting Started with aloop" documentation set covering
quickstart through advanced configuration. A developer should go from zero
to running agent in under 10 minutes.

**One-Sentence Summary**:
> A 5-page documentation set that takes a developer from "what is this?" to
> "my agent is running and improving" in under 10 minutes.

## Success Criteria (in priority order)
- [ ] **Quickstart guide** — deploy in <10 minutes, 3 commands (NON-NEGOTIABLE, goes first)
- [ ] Concepts overview — what is aloop, the loop pattern, why it works
- [ ] Tutorial — build your first autonomous research agent
- [ ] How-to — write effective steering.md files
- [ ] How-to — monitor and debug your agent (logs, progress.json)
- [ ] Reference — steering.md schema with all fields documented
- [ ] Reference — environment variables and configuration
- [ ] All code examples are copy-paste runnable
- [ ] Troubleshooting section for top 5 failure modes
- [ ] 4000-8000 words total across all pages
- Score target: 90/100

## Constraints
- Follow Microsoft Learn style guide (2nd person, active voice, task-oriented)
- Output files: artifacts/docs/ directory with separate files per page
- Use consistent heading hierarchy
- Include expected output after commands where possible

## Instructions to Agent
- IMPORTANT: Write EACH doc page in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- The quickstart is the front door. If it's confusing, nothing else matters.
  Test every command in your head — does it actually work?
- Use the azd template as the basis for all examples.
- Include both Azure CLI and Portal paths where relevant.
- Each code block should specify the language for syntax highlighting.
- Cross-link between pages.
- DO NOT RAMBLE. If a paragraph doesn't help the reader complete a task, cut it.

## Loop Settings
- interval_minutes: 12
- max_iterations: 20
- abort: false
