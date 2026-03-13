# aloop

**Describe what you want in plain text. An AI agent relentlessly refines it overnight. You wake up to the finished version.**

aloop deploys an autonomous AI agent into the cloud. You write plain-text instructions. The agent plans, executes, scores its own work 0–100, throws away anything that doesn't improve on the best, and loops — all without you touching it again.

You don't babysit it. You don't re-prompt. You walk away and let iteration do what iteration does.

> **Read more:** [aloop: An AI Agent That Works While You Sleep](loops/blog-writer/sample-output.md) — a blog post written and refined by aloop's blog-writer demo.

## Quick Start

```bash
git clone https://github.com/Azure-Samples/aloop
cd aloop
aloop start
```

The CLI walks you through setup — picks a loop type, offers a ready-to-run demo, deploys the infrastructure, and starts the agent. No flags, no config files.

### Prerequisites

- [Azure Developer CLI (`azd`)](https://aka.ms/azd-install)
- [Azure CLI (`az`)](https://aka.ms/install-azure-cli)
- [Azure subscription](https://azure.microsoft.com/free)

Don't have these installed? `aloop` checks automatically and shows install links.

## How It Works

```
Read steering.md → Plan → Execute → Evaluate (0-100) → Gate (keep or discard)
       ↑                                                        │
       └──────────────── sleep N minutes ───────────────────────┘
```

Each iteration, the agent:

1. **Reads** your instructions from `steering.md` (fresh every pass — you can steer mid-run)
2. **Plans** a measurable action with an evaluation rubric
3. **Executes** the plan using tools (write files, search the web, run Python)
4. **Evaluates** its own output against the rubric (0–100, per-criterion breakdown)
5. **Gates** — keeps the result only if `score > best_score` (strict improvement, no sideways drift)

Then it sleeps and does it again. The best artifact survives. Everything else is discarded.

## CLI Commands

```bash
aloop start      # deploy and start the agent
aloop steer      # upload revised instructions to running agent
aloop stop       # graceful shutdown
aloop status     # check progress (default command)
aloop download   # pull finished artifacts to ./output/
aloop            # same as status
```

Here's what `aloop` looks like when you check on a running loop:

```
$ aloop

  aloop status
  ────────────────────────────────
  Loop:       blog-writer
  Iteration:  14 / 25
  Best score: 88 (iteration 6)
  Status:     RUNNING
  Last score: 76 (discarded)
  ────────────────────────────────
  Scores: 86 → 83 → 85 → 74 → 72 → 88 → 86
          → 74 → 86 → 78 → 88 → 78 → 78 → 76

  Run aloop download to grab the best artifact.
  Run aloop steer to update instructions.
```

## Steer While It Runs

The agent and you work on your own schedules. The agent loops continuously, improving the work. You can check in whenever you want and *steer* — edit the instructions, raise the bar, change direction. Run `aloop steer` and the agent picks up your changes on its next pass. No restart, no redeploy, no lost progress.

```
You (evening):   "Write a blog post about aloop for developers and non-developers"
Agent (overnight): drafts, scores, keeps best → 86 → 83 → 85 → 74 → 72 → 88 ✓

You (next day):  "Show the steering pattern, make it less abstract"
Agent (afternoon): incorporates feedback → 86 → 78 → 88 → matched peak
```

Two independent loops — human steering and AI iteration — converging on something good without either side waiting on the other.

## Loop Types

Each loop type has a **template** (`steering.md` with placeholders) and a **demo** (a ready-to-run example). The CLI offers to use the demo so you can see results immediately.

| Loop Type | What It Produces | Demo |
|-----------|-----------------|------|
| [blog-writer](loops/blog-writer/) | Polished articles refined across iterations | aloop writing about itself |
| [deep-research](loops/deep-research/) | Multi-source analysis with citations | Anthropic Messages API vs OpenAI & Azure SDKs |
| [spec-writer](loops/spec-writer/) | PRDs and design documents | aloop product specification |
| [sample-builder](loops/sample-builder/) | Working code with tests | AI Meeting Notes Summarizer |
| [sdk-review](loops/sdk-review/) | Developer experience assessments | Foundry/Azure AI SDKs vs OpenAI/LangChain & 3P OSS |
| [slide-deck](loops/slide-deck/) | Presentations with speaker notes | Conference talk on autonomous loops |
| [changelog-writer](loops/changelog-writer/) | Release notes from change summaries | OpenAI SDK for .NET v2.2.0 |
| [data-analysis](loops/data-analysis/) | Survey analysis with visualizations | Developer survey analysis |
| [doc-writer](loops/doc-writer/) | Complete documentation sets | Getting Started with aloop |
| [strategic-planning](loops/strategic-planning/) | Prioritization with RICE scoring | Azure AI Agent Platform H2 2026 |

The common thread: any task where a twenty-fifth draft beats a first draft.

## Why Iteration Beats One-Shot

When you prompt ChatGPT or a deep-research tool, you get one response. If it's 80% of what you wanted, *you* close the gap.

aloop flips that. The agent closes the gap:

```
Iteration  1: 86/100 — decent structure, weak opening
Iteration  3: 85/100 — tried restructuring, evaluator rejected it
Iteration  5: 72/100 — overcorrected, threw it away
Iteration  6: 88/100 — concrete examples, better flow (new best)
Iteration 11: 88/100 — matched best after steering update
Iteration 20: 88/100 — sixth time hitting peak score
```

The agent tried 25 different versions. Most scored lower and were thrown away. Only the strongest survived. That competitive selection is the mechanism — not any single brilliant generation, but the accumulated effect of many attempts filtered by honest self-evaluation.

Five minutes writing instructions buys you hours of autonomous improvement.

## steering.md Format

```markdown
## Goal
What you want the agent to achieve.

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- Score target: 90/100

## Constraints
- Output file: artifacts/my-output.md

## Instructions to Agent
Specific guidance, tone, focus areas.

## Loop Settings
- interval_minutes: 10
- max_iterations: 25
- abort: false
```

## Architecture

```
┌──────────────────────────────────────────────────┐
│           Azure Container Apps                    │
│  ┌──────────────────────────────────────────┐    │
│  │  Read steering → Plan → Execute → Score  │    │
│  │       ↑         keep best, discard rest  │    │
│  │       └──────── sleep N min ─────────┘   │    │
│  └──────────────────────────────────────────┘    │
│  Azure Blob Storage        Azure OpenAI          │
└──────────────────────────────────────────────────┘
```

- **Compute**: Azure Container Apps (single replica, 1 CPU / 2GB)
- **Model**: Azure OpenAI via the Responses API
- **Storage**: Azure Blob Storage (passwordless auth via managed identity)
- **Deploy**: `azd up` with Bicep templates in `infra/`

## Project Structure

```
aloop                       # Bash CLI entry point
azure.yaml                  # azd service definition
steering.md                 # Your instructions (overwritten by CLI)

src/agent/
  loop.py                   # Main loop orchestrator
  config.py                 # Env-var configuration
  planner.py                # Plan generation from steering + history
  executor.py               # Tool-calling execution
  evaluator.py              # Rubric-based scoring (0-100)
  model_client.py           # Azure OpenAI Responses API client
  storage.py                # Azure Blob / local filesystem abstraction
  steering.py               # steering.md parser
  tools.py                  # Agent tool definitions

infra/
  main.bicep                # Top-level infrastructure
  modules/                  # ACA, identity, OpenAI, storage modules

loops/                      # 10 loop types, each with template + demo
```

## Extending

**Add a loop type**: Create `loops/my-type/steering.md` (template with `[PLACEHOLDER]` fields) and `loops/my-type/demo.md` (concrete example). The CLI auto-discovers it.

**Add a tool**: Add the OpenAI function schema to `TOOL_DEFINITIONS` in `tools.py`, implement `_tool_my_tool()`, and add the dispatch case in `execute_tool()`.

**Run locally**: Set `LOCAL_MODE=true` and `LOCAL_WORKSPACE=./workspace` to use the local filesystem instead of Azure Blob.

## Inspirations

- [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) — keep-or-discard gating
- [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) — single agent with good tools
- [Ralph Loop](https://en.wikipedia.org/wiki/OODA_loop) — self-referential iteration

## Advanced

### Tuning iterations, sleep, and score target

All loop behavior is controlled in the `## Loop Settings` section of `steering.md`:

```markdown
## Loop Settings
- interval_minutes: 5      # sleep between iterations (default: 10)
- max_iterations: 50        # how many attempts (default: 25)
- target_score: 95          # stop early if this score is reached
- abort: false              # set to true for graceful shutdown
```

These are read fresh every iteration, so you can change them mid-run with `aloop steer`.

### Changing the model

The model is set at deploy time via the `azd` environment:

```bash
azd env set AZURE_OPENAI_DEPLOYMENT gpt-4o
aloop start
```

To change the model on a running deployment, update the environment variable and redeploy with `azd up`.

### Running multiple loops in parallel

Each `azd` environment is an independent deployment with its own storage, compute, and model. To run multiple loops simultaneously, create separate environments:

```bash
# Loop 1: blog writer
azd env new blog-loop
aloop start                    # picks blog-writer, deploys to blog-loop

# Loop 2: deep research (in a separate terminal)
azd env new research-loop
azd env select research-loop
aloop start                    # picks deep-research, deploys to research-loop
```

Each loop gets its own Azure Container App, storage account, and blob container. They run independently and don't interfere with each other. Check on any loop by selecting its environment first:

```bash
azd env select blog-loop
aloop status

azd env select research-loop
aloop download
```

## License

MIT — see [LICENSE](LICENSE).
