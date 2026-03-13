# Sample App Builder Demo — AI Meeting Notes Summarizer

## Goal
Build a complete, runnable sample application: "AI Meeting Notes Summarizer"
that uses Azure OpenAI to summarize meeting transcripts, extract action items,
and generate follow-up emails. Package as an azd template.

**One-Sentence Summary**:
> A FastAPI app that takes a meeting transcript and returns a summary, action
> items, and a draft follow-up email — runnable with one command.

## Success Criteria (in priority order)
- [ ] **Working code that runs** — clone, install, run, get output (NON-NEGOTIABLE)
- [ ] POST /summarize endpoint that accepts transcript text
- [ ] Returns: summary, action items, follow-up email draft
- [ ] README with setup instructions and example request/response
- [ ] Clean code with type hints
- [ ] At least 3 unit tests passing (mock responses, not live API)
- [ ] Dockerfile for containerization
- [ ] Example transcript in test data
- [ ] Minimal dependencies
- Score target: 90/100

## Constraints
- Use the OpenAI Python SDK (not REST)
- Use FastAPI for the web framework
- Output files: artifacts/sample-app/ directory
- Keep dependencies minimal

## Instructions to Agent
- IMPORTANT: Write EACH source file in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- The README is as important as the code. A brilliant app nobody can run is worthless.
- DO NOT OVER-ENGINEER. A working app with 3 files beats an elegant app with 15.
- Use GPT-5.3-chat for the summarization.
- Follow Azure SDK guidelines for error handling.
- Make the README beginner-friendly — assume the reader has never used FastAPI.

## Loop Settings
- interval_minutes: 10
- max_iterations: 20
- abort: false
