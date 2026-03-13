# SDK Review Demo — Foundry/Azure AI SDKs vs OpenAI, LangChain & 3P OSS AI SDKs

## Goal
Review the Azure AI Foundry SDK and Azure AI Inference SDK against the OpenAI
Python SDK, LangChain, and other popular third-party OSS AI SDKs. Produce a
developer experience assessment with specific, actionable feedback for the
Azure AI SDK team.

**One-Sentence Summary**:
> A brutally honest DX comparison of Azure AI SDKs against OpenAI, LangChain,
> and other popular OSS alternatives — with prioritized recommendations the
> Azure team can act on this sprint.

## Success Criteria (in priority order)
- [ ] **Top 10 prioritized recommendations for Azure AI SDKs** (NON-NEGOTIABLE, goes first)
- [ ] "First 5 minutes" experience assessment for each SDK ecosystem
- [ ] API surface inventory (key classes, methods, patterns) for Azure AI Foundry, OpenAI, LangChain
- [ ] Side-by-side code comparison for 3 common scenarios (chat completion, tool calling, RAG)
- [ ] Error handling and debugging experience comparison
- [ ] Documentation quality and discoverability assessment
- [ ] Package ecosystem: how easy is it to compose with other libraries?
- [ ] Missing features or gaps in each
- [ ] 2000-4000 words
- Score target: 85/100

## Constraints
- Be brutally honest — this is internal feedback, not marketing
- Output file: artifacts/sdk-review.md
- Use publicly available docs and PyPI/npm packages
- Every criticism must include a specific fix suggestion
- Cover at minimum: azure-ai-inference, azure-ai-projects, openai, langchain, plus 1-2 others

## Instructions to Agent
- IMPORTANT: Write the ENTIRE review in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with the recommendations. The team wants to know what to fix.
- Try to install and import the SDKs if possible (run_python).
- Write sample code for: chat completion, tool calling, RAG pipeline.
- Focus on what a new developer would struggle with in the first hour.
- Compare naming conventions, error messages, type hints quality, package size.
- Assess the "OpenAI compatibility" story — can Azure SDKs be a drop-in?
- DO NOT RAMBLE. Cite specific classes, methods, and error messages.

## Loop Settings
- interval_minutes: 12
- max_iterations: 18
- abort: false
