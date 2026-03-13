# aloop — Copilot Instructions

## Project Identity

- **Name**: aloop (always lowercase, never "LoopAgent", "loop-agent", or "Aloop")
- **What it is**: An autonomous AI agent that reads plain-text instructions, iteratively improves its work, and runs unattended in the cloud
- **Tagline**: Describe what you want in plain text. An AI agent relentlessly refines it overnight. You wake up to the finished version.
- **Repo**: `Azure-Samples/aloop`
- **License**: MIT

## Architecture

The agent runs a 5-phase iteration cycle:

```
Read steering.md → Plan → Execute → Evaluate (0-100) → Gate (keep or discard)
       ↑                                                        │
       └──────────────── sleep N minutes ───────────────────────┘
```

### Phase Details

1. **Read** — Load `steering.md` fresh every iteration (enables live steering). Check abort signal.
2. **Plan** — `planner.py` generates a measurable action plan with evaluation rubric, using iteration history to avoid repeating failures.
3. **Execute** — `executor.py` calls the model with tools. The executor always receives the current best artifact and improves it incrementally (never starts from scratch).
4. **Evaluate** — `evaluator.py` scores the output 0-100 against the plan's rubric. Produces per-criterion breakdown + critique.
5. **Gate** — Strict improvement only: `score > best_score` (never `>=`). Lower or equal scores are discarded. This prevents lateral drift.

### Key Design Decisions

- **Strict `>` gating** — Equal scores are discarded. This was a bug fix; `>=` allowed sideways drift where the agent churned without real improvement.
- **Full artifact to evaluator** — The evaluator sees the complete artifact, not a truncated version. Truncation caused phantom high scores on incomplete work.
- **Best artifact to executor** — The executor always receives the highest-scoring artifact as its baseline. Without this, it would sometimes start fresh and regress.
- **Fresh steering every iteration** — Enables humans to steer mid-run without restarting.
- **Append-only iteration log** — `iteration_log.jsonl` is never overwritten, providing full history for debugging.
- **Self-healing progress** — If `progress.json` is corrupt (JSON decode error), the agent resets to defaults and continues rather than crash-looping.

## File Structure

```
aloop                       # Bash CLI — the user-facing entry point
azure.yaml                  # azd service definition
steering.md                 # Working steering file (overwritten by CLI)
README.md                   # Project documentation

src/agent/
  loop.py                   # Main loop orchestrator (entry point)
  config.py                 # Environment-variable-based configuration
  planner.py                # Plan generation from steering + history
  executor.py               # Tool-calling execution of plans
  evaluator.py              # Rubric-based scoring (0-100)
  model_client.py           # Azure OpenAI Responses API client
  storage.py                # Storage abstraction (Azure Blob / local)
  steering.py               # steering.md parser
  tools.py                  # Agent tool definitions and implementations
  Dockerfile                # Container image build
  requirements.txt          # Python dependencies

infra/
  main.bicep                # Top-level Azure infrastructure
  main.parameters.json      # azd parameter substitution
  modules/
    aca.bicep               # Container Apps + ACR + Log Analytics
    identity.bicep           # User-assigned managed identity
    openai.bicep            # Azure OpenAI + model deployment
    storage.bicep           # Storage account + blob container

loops/                      # Loop type library (10 types)
  blog-writer/              # Each has steering.md (template) + demo.md
  deep-research/
  spec-writer/
  slide-deck/
  sdk-review/
  sample-builder/
  changelog-writer/
  data-analysis/
  doc-writer/
  strategic-planning/

output/                     # Local download target for artifacts
```

## Key Conventions

### Naming
- Project is always **aloop** (lowercase) in code, docs, CLI output, and user-agent strings
- Logger name: `"aloop"` in all Python modules
- Container name in ACA: `loop-agent` (infrastructure-level, not user-facing)

### Azure Resources
- Deployed via `azd up` using Bicep templates in `infra/`
- Passwordless auth everywhere: `DefaultAzureCredential` + managed identity
- Storage: Azure Blob Storage with `Storage Blob Data Contributor` role
- Model: Azure OpenAI with `Cognitive Services OpenAI User` role
- Container: Azure Container Apps, single replica, 1 CPU / 2GB memory

### Model Client
- Uses **OpenAI Responses API** (`client.responses.create()`), NOT chat completions
- Tool-calling loop runs up to 15 rounds per execution
- Auth: Bearer token via `azure.identity.get_bearer_token_provider`

### Storage Paths (in blob container `agent-workspace`)
- `steering.md` — control file (uploaded by user)
- `artifacts/*` — agent output (e.g., `artifacts/blog-post.md`)
- `progress.json` — current state: scores array, best_score, total_iterations, status
- `iteration_log.jsonl` — append-only log of every iteration
- `reports/iteration_NNN.md` — detailed per-iteration reports
- `reports/latest.md` — most recent report

### Steering Format
```markdown
## Goal
What the agent should achieve.

## Success Criteria
- [ ] Criterion 1
- Score target: 90/100

## Constraints
- Output file: artifacts/my-output.md

## Instructions to Agent
Specific guidance for execution.

## Loop Settings
- interval_minutes: 10
- max_iterations: 25
- abort: false
```

## How to Extend

### Adding a New Loop Type
1. Create `loops/my-type/steering.md` — generic template with `[PLACEHOLDER]` fields
2. Create `loops/my-type/demo.md` — concrete ready-to-run example
3. The CLI auto-discovers new directories in `loops/`

### Adding a New Tool
1. Add tool definition to `TOOL_DEFINITIONS` list in `tools.py` (OpenAI function-call schema)
2. Add implementation function `_tool_my_tool()`
3. Add dispatch case in `execute_tool()`

### Local Development
Set `LOCAL_MODE=true` and `LOCAL_WORKSPACE=./workspace` to run against local filesystem instead of Azure Blob.

## Common Pitfalls (Lessons Learned)

1. **JSON crash loops** — If blob storage returns empty/corrupt JSON, the agent must handle it gracefully. All JSON reads go through `storage.read_json()` which has try/except.
2. **Evaluator truncation** — Never truncate the artifact before sending it to the evaluator. Truncated artifacts score artificially high because the evaluator can't see what's missing.
3. **Gate operator** — Use strict `>`, never `>=`. Equal scores mean the agent is churning sideways, not improving.
4. **Executor baseline** — Always pass the best artifact to the executor. Without it, the executor may start from scratch and produce worse output.
5. **Progress file atomicity** — Write to a temp path then overwrite, or handle partial writes. The agent writes progress.json via `storage.write_json()` which handles this.

## CLI Commands
```bash
aloop start      # Deploy infrastructure and start the agent
aloop steer      # Upload revised steering.md to running agent
aloop stop       # Graceful shutdown (sets abort: true)
aloop status     # Show progress (default when run with no args)
aloop download   # Pull artifacts to ./output/
aloop            # Same as status
```
