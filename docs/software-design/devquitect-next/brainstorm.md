# Devquitect Next brainstorm

## 2026-09-21 — Seed and scope

The user asked to compare two complementary proposals: a GPT-5.6-oriented simplification of Devquitect skill instructions, and a lightweight QUICK workflow for small localized changes. The resulting direction is one staged program with separate delivery concerns rather than one merged skill.

Confirmed baseline evidence:

- `software-idea-to-project`, `project-plan-execution`, and `targeted-refactoring` have intentionally distinct authority boundaries.
- `project-plan-execution` is for approved persistent-plan slices; QUICK must not broaden that contract.
- `verify_slice.py` is distributed to consumer repositories and currently requires Python 3.12+ and PyYAML.
- GPT-5.6 guidance favors leaner prompts, single ownership of instructions, explicit autonomy boundaries, and representative evaluation after each simplification.

The user approved persistent definition work for the sequence 0.7.0, 0.8.0, and 1.0.0. No implementation was authorized.

## 2026-09-21 — Gate 1 and technical direction

The user approved Gate 1. The proposed fourth `devquitect` routing skill was rejected as premature overhead. QUICK remains an independent skill: its concise description enables implicit activation for eligible local changes and direct invocation remains available. A consumer repository may add a short routing rule to its `AGENTS.md` when it needs stronger local routing guidance.

An earlier technical-design direction considered JSON and a stdlib-only Python verifier path. It was later removed: verify_slice remains unchanged in this initiative.

## 2026-09-22 — Gate 2 and delivery plan

The user approved Gate 2. The delivery plan separates six coherent slices across the three releases: lean entrypoints and QUICK for 0.7.0; JSON verification and legacy migration for 0.8.0; then stability evidence and release readiness for 1.0.0. The plan is not implementation authorization.

## 2026-09-22 — Formal v2 scope expansion

The user expanded Devquitect Next to cover the full v2 direction: a phased prompt-change protocol, workflow depth for every initiative, detected or configured durable roots, explicit invocation policy, and a comparable multi-model/host evaluation matrix. Gate 1, Gate 2, and the unapproved implementation plan were invalidated because these changes broaden product and technical contracts.

The intended prompt-change ledger will not copy original or candidate prompts. Every entry instead records immutable source snapshot identities, affected paths and rule groups, retain/move/remove disposition, cases, model/host configuration, report references, and verdict; Git and snapshots reconstruct the exact text.

## 2026-09-22 — Amended Gate 1 review

The expanded definition is ready for review. The proposed ledger is intentionally a small versioned Markdown record, not a second prompt store or a new evaluator schema: existing snapshots, Git references, authority owners, comparison reports, and calibration reports remain authoritative.

## 2026-09-22 — Cross-generation model matrix amendment

The user asked to adjust Devquitect Next after OpenAI announced GPT-6 Sol and GPT-6 Luna. The proposed matrix retains GPT-5.6 Sol/Terra/Luna as prior-generation comparison rows and adds GPT-6 Sol (`gpt-6-sol`) and GPT-6 Luna (`gpt-6-luna`) as separate rows. Model, host, runtime, reasoning effort where supported, suite revision, and repetitions remain explicit; results are not pooled. The source is [OpenAI's GPT-6 Sol and Luna announcement](https://openai.com/index/introducing-gpt-6-sol-and-luna/), which states API IDs and Codex availability.

This changes the scope of evaluation evidence and affects `SLICE-DN-004`, but does not change user-facing workflows, authority boundaries, or verifier behavior. No behavioral evaluation or implementation is authorized.

## 2026-09-22 — Gate 1 approval for cross-generation coverage

The user approved the amended Gate 1 definition: GPT-5.6 Sol/Terra/Luna remain baseline rows and GPT-6 Sol/Luna are added as separate rows. This approves design scope only. Technical details proceed to Gate 2 review; it does not authorize behavioral comparisons or implementation slices.

## 2026-09-22 — Cross-generation technical design ready

The technical design fixes the initial model IDs to `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`. Each independent evidence row records host, runtime, reasoning effort where supported, case-suite revision, repetitions, and report references. It reuses the existing prompt-change ledger fields and makes no evaluator-schema or verifier changes. If host, runtime, or effort differs, the row remains distinct and supports no model-only claim. The architecture, data, and interface updates are ready for Gate 2 review; plan revision 2 remains Review pending Gate 2. No behavioral evaluation or implementation is authorized.

## 2026-09-22 — Gate 2 approval and plan revision 2

The user approved Gate 2. The approved technical design uses the existing prompt-change ledger and verifier boundary, with no new evaluator schema or migration. The plan revision 2 update will revise `SLICE-DN-004` and its evidence acceptance criterion to include the five approved model IDs and preserve separate, attributable verdicts. No implementation or behavioral comparison is authorized.

## 2026-09-22 — Plan revision 2 ready for approval

`SLICE-DN-004` and `AC-DN-008` now specify the five model IDs, one declared model/host/runtime/reasoning/suite/repetitions/report tuple per row, use of the same prompt-change group and representative cases, separate verdicts, and no behavioral run without separate authorization. Plan revision 2 remains Review pending the user's explicit plan approval. No implementation slice is authorized.

## 2026-09-22 — Plan revision 2 approved

The user approved only implementation plan revision 2. This completes the persistent definition workflow; it does not authorize implementation, behavioral comparisons, or any `SLICE-DN-*` execution. Future delivery requires a separate explicit authorization naming the slices.
