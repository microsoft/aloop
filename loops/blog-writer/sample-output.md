---
title: "aloop: An AI Agent That Works While You Sleep"
author: aloop project
date: 2026-03-13
tags: ai, agents, azure, openai, automation, aloop
---

# aloop: An AI Agent That Works While You Sleep

Last Tuesday I wrote six bullet points in a text file describing the blog post I wanted. I ran one command and went to dinner.

By morning, an AI agent had written the post, scored its own work, thrown away the weaker drafts, and kept improving the strongest version — 25 times — while I slept. The result scored 88/100.

This is that post. And the tool that wrote it is called **aloop**.

## What aloop Does

aloop gives anyone access to the power of AI agents — no coding, no frameworks, no orchestration logic. You write plain-text instructions. aloop handles the rest.

```bash
aloop start      # deploy the agent
aloop steer      # send your instructions
aloop             # check progress
aloop download   # grab the finished work
```

The agent runs in the cloud on Azure Container Apps, calling Azure OpenAI models in a loop. Each iteration it plans, executes, reviews its own work with a score from 0–100, and keeps only the version that improves on the last.

You don't babysit it. You don't re-prompt. You walk away and let iteration do what iteration does. But you *can* peek in anytime — run `aloop` to check the score, and `aloop steer` to nudge direction mid-run. The agent picks up your changes on its next pass without restarting.

## The Steering Pattern

Here's what makes aloop different from a chatbot or a one-shot AI tool: **you and the agent work on your own schedules.**

The agent loops continuously, improving the work. Meanwhile, you can check in whenever you want and *steer* — edit the instructions, raise the bar, change direction. The agent picks up your changes on its next pass. No restart, no redeploy, no lost progress.

Here's exactly how that played out for this post:

I ran `aloop start`, picked the blog-writer demo, and went to dinner. When I checked back, the first draft had scored 86/100 — decent structure, but the opening paragraph was:

> *"This article explains an autonomous agent architecture deployed on Azure infrastructure."*

Technically accurate. Completely lifeless. The next few iterations tried restructuring and scored lower — 83, 85, 74. The agent threw all of those away.

Then on iteration 6, it rewrote the opening to start with a person doing something — writing bullets, closing a laptop, waking up to results. Score jumped to 88. Same information, better framing.

I ran `aloop steer` and added a note: "Show the steering pattern itself — the reader should understand that human and AI work independently." The agent picked that up on its next pass. Some iterations scored lower and were discarded. Others matched the 88 peak. Over 25 iterations, the best version survived.

```
You (evening):   "Write a blog post about aloop for developers and non-developers"
Agent (overnight): drafts, scores, keeps best → 86 → 83 → 85 → 74 → 72 → 88 ✓

You (next day):  "Show the steering pattern, make it less abstract"
Agent (afternoon): incorporates feedback → 86 → 78 → 88 → matched peak
```

**The AI changes stuff on its own, you change stuff on your own.** Two independent loops — human steering and AI iteration — converging on something good without either side waiting on the other.

## Beyond Blog Posts

Writing is the easiest demo to show. But the same pattern — iterate, evaluate, keep the best — works for anything where revision improves quality.

**Research and analysis.** Describe a question. The agent searches, synthesizes, critiques its own reasoning, and produces a report that gets sharper with every pass. A 25-iteration research loop covers more ground than any single query.

**Code and applications.** Point aloop at a scaffold and tell it to build a small web app or utility. The agent writes code, runs tests, evaluates whether they pass, and keeps iterating. It works best when the evaluation is concrete — test suites, linting, build success — so the agent knows when it's improving.

**Specs, slide decks, strategic plans.** aloop ships with 10 loop types out of the box. The big three:

- **Deep research** — multi-source analysis with citations, iteratively fact-checked
- **Code samples** — working code with tests, refined until they pass
- **Spec writer** — structured technical specifications that tighten with each pass

Plus blog posts, changelogs, SDK reviews, data analysis, documentation, slide decks, and strategic plans — each with a ready-to-run demo you can try in minutes.

The common thread: any task where a twenty-fifth draft beats a first draft.

## Why Iteration Beats One-Shot

When you use ChatGPT or a deep-research tool, you get one response. If it's 80% of what you wanted, *you* close the gap.

aloop flips that. The agent closes the gap. Here's what that looks like in practice — the actual score progression from the run that produced this post:

```
Iteration  1: 86/100 — decent structure, weak opening
Iteration  3: 85/100 — tried restructuring, evaluator rejected it
Iteration  5: 72/100 — overcorrected, threw it away
Iteration  6: 88/100 — concrete examples, better flow (new best)
Iteration 11: 88/100 — matched best after steering update
Iteration 20: 88/100 — sixth time hitting peak score
```

The agent tried 25 different versions. Most scored lower and were thrown away. Only the strongest survived. That competitive selection is the mechanism — not any single brilliant generation, but the accumulated effect of many attempts filtered by honest self-evaluation.

The result isn't a first draft. It's the best of twenty-five drafts, shaped by both AI iteration and human steering along the way.

Your time is the expensive resource. Five minutes writing instructions buys you hours of autonomous improvement.

## Try It

```bash
git clone https://github.com/Azure-Samples/aloop
cd aloop
aloop start
```

[View the repo on GitHub →](https://github.com/Azure-Samples/aloop)

The CLI walks you through setup — picks a loop type, offers a ready-to-run demo, deploys the infrastructure, and starts the agent. Edit `steering.md` with your own goal and run `aloop steer` whenever you want to change direction.

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

That's it. Describe what you want. Let the agent work. Wake up to the result.

I wrote six bullets and went to dinner. The agent handled the next twenty-five iterations.
