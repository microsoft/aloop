# Sample App Builder

## Goal
Build a complete, runnable sample application: **[YOUR APP, e.g., "AI Meeting
Notes Summarizer" or "Customer Feedback Classifier"]**. Package it so someone
can clone and run it in under 5 minutes.

**One-Sentence Summary**:
> [e.g., "A FastAPI app that summarizes meeting transcripts, extracts action
> items, and drafts follow-up emails — runnable with one command."]

## Success Criteria (in priority order)
- [ ] **Working code that runs** — clone, install, run, get output (NON-NEGOTIABLE)
- [ ] README with setup instructions and example request/response
- [ ] Clean code with type hints and clear naming
- [ ] At least 3 unit tests passing
- [ ] Dockerfile for containerization
- [ ] Minimal dependencies — don't add libraries you don't need
- [ ] Error handling for common failure modes (auth, rate limits, bad input)
- Score target: 90/100

## Constraints
- Output files: artifacts/sample-app/ directory
- Keep dependencies minimal — justify every pip install
- Tests must use mocks, not live API calls

## Instructions to Agent
- IMPORTANT: Write EACH source file in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- The README is as important as the code. A brilliant app nobody can run is
  worthless. Include: what it does, how to run it, example input/output.
- DO NOT OVER-ENGINEER. No abstraction layers, no plugin systems, no config
  frameworks. A working app with 3 files beats an elegant app with 15.
- Write for two audiences: the runner (README, Dockerfile, quick commands) and
  the reader (clean code, good names, comments only where not obvious).
- If you add a dependency, use it. If you import it and only call it once,
  inline it instead.

## Loop Settings
- interval_minutes: 10
- max_iterations: 20
- abort: false
