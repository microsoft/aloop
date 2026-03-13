# Spec Writer Demo — aloop Product Specification

## Goal
Write the product specification for **"aloop: Autonomous Agent Hosting on Azure
Container Apps"** — a technical and product spec for the aloop project itself.

**One-Sentence Summary**:
> A complete product spec that would let a developer team understand, build, and
> ship aloop from scratch, including architecture, security model, and DX design.

## Success Criteria (in priority order)
- [ ] **Problem Statement** — why one-shot AI isn't enough, framed for product teams (NON-NEGOTIABLE)
- [ ] Architecture Overview — ACA + Azure OpenAI + Blob, mermaid diagram
- [ ] Developer Experience walkthrough — from `azd up` to `aloop download`
- [ ] Steering file spec — format, fields, constraints
- [ ] Loop lifecycle — plan → execute → evaluate → gate → sleep → repeat
- [ ] Security model — RBAC, managed identity, no keys in env, blob isolation
- [ ] Failure modes — crash recovery, self-healing progress, max-iteration ceiling
- [ ] Cost model — per-loop estimates, idle cost, burst cost
- [ ] Open questions — explicit list of unresolved design decisions
- [ ] Glossary — steering, artifact, gate, loop, iteration
- Score target: 85/100

## Constraints
- 2000-3000 words
- Output file: artifacts/spec.md
- Mixed audience: PM who approves + engineer who builds + security reviewer who blocks
- Use markdown tables for structured comparisons
- Include mermaid diagrams for architecture and lifecycle

## Instructions to Agent
- IMPORTANT: Write the FULL spec in a single write_file call. Do NOT truncate.
- Before rewriting, ALWAYS read existing artifacts first. Build on what you have.
- Lead with the problem. The reader must feel the pain before you describe the fix.
- Architecture diagram is NON-NEGOTIABLE. Use mermaid.
- Every section: say what it is, why it matters, and how it works.
- Security model earns trust. Be specific: "managed identity, not API key" — not "secure by default."
- Open Questions section is mandatory. Honest gaps beat false confidence.
- DO NOT RAMBLE. Every paragraph must survive "does this help the reader build it?"
- Cost model: real numbers or formulas, not "it depends."

## Loop Settings
- interval_minutes: 12
- max_iterations: 20
- abort: false
