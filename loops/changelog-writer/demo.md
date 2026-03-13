# Changelog Writer Demo — OpenAI SDK for .NET v2.2.0

## Goal
Generate professional release notes for **openai-dotnet v2.2.0** (the official
OpenAI SDK for .NET, github.com/openai/openai-dotnet) by synthesizing a set of
changes into user-facing documentation that .NET developers actually want to read.

**One-Sentence Summary**:
> Release notes for openai-dotnet v2.2.0 — covering new Responses API support,
> streaming improvements, bug fixes, and a breaking change with migration guidance.

## Success Criteria (in priority order)
- [ ] **Highlights section** — top 3 changes, front and center (NON-NEGOTIABLE, goes first)
- [ ] Categorized: New Features, Improvements, Bug Fixes, Breaking Changes
- [ ] Each entry has a user-facing description — explain the "why", not just the "what"
- [ ] Breaking changes include step-by-step migration guidance with C# code examples
- [ ] Links to relevant API reference placeholders
- [ ] Scannable — bullet-point format, bold key terms
- [ ] Professional tone matching real .NET SDK changelogs
- [ ] 500-1500 words
- Score target: 88/100

## Constraints
- Follow Keep a Changelog format
- Output file: artifacts/release-notes.md
- Include at least: 2 new features, 3 improvements, 2 bug fixes, 1 breaking change
- Use realistic .NET/C# API surface names (e.g., ChatClient, OpenAIClient, ResponsesClient)

## Instructions to Agent
- IMPORTANT: Write the ENTIRE changelog in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Invent realistic but clearly fictional changes for the openai-dotnet SDK.
- The highlights section is the front door — most readers stop there. Make it count.
- Each entry should explain impact, not just describe the change. "Reduced token
  counting overhead by 60% for streaming responses" beats "Improved performance."
- Include C# code snippets for breaking changes and key new features.
- DO NOT RAMBLE. Brevity is a feature in release notes.

## Loop Settings
- interval_minutes: 8
- max_iterations: 12
- abort: false
