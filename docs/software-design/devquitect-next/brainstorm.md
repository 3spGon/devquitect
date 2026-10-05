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

## 2026-10-02 — Continuous Verification and Release Readiness amendment

The user supplied the initiative to redefine DN-005 around clean-runner Continuous Verification and DN-006 around exact-candidate Release Readiness, then explicitly requested `software-idea-to-project` to make the necessary plan changes. This authorizes a persistent review amendment, not implementation or new gate approvals. Plan revision 3 is Review; concept/requirements/decisions are Review; affected technical documents are Draft for confirmation after amended Gate 1.

The affected baseline was revalidated against the current checkout. No `.github/workflows/` implementation exists. Existing credential-free checks, platform-sensitive tests, packaging, and release policy are available. The packager already rejects requested/committed version mismatch: the earlier analysis's claim that it rewrites the version was incorrect. `release-check` rebuilds twice and binds canonical check evidence to the exact commit/snapshot, but does not take a CI ZIP directly and currently uses the immediate parent for version compatibility.

The review direction preserves local verification, separates manual authorized behavioral evidence from required deterministic gates, reruns CI for the final integrated SHA, and requires GitHub provenance plus file-digest/package identity. It proposes a compatible explicit previous-release reference so post-bump fixes can be release candidates. Effective main protection and successful real runner evidence remain delivery requirements; documentation or local fixtures alone do not prove them. Optional behavioral infrastructure failure is inconclusive and does not block a deterministically correct PR.

Only DN-005 and DN-006 change. Existing AC-DN-009 through AC-DN-012 keep their meanings; AC-DN-013 through AC-DN-023 add the new guarantees. DN-001 through DN-004 and their inventory are unchanged. The revision-2 delivery checkpoint and slice evidence remain untouched and authoritative for that delivery. Future authorized execution must reconcile revision 3 explicitly rather than imply that earlier evidence satisfies changed future criteria.

The profile remains confirmed full / rigorous and cross-cutting, now explicitly covering external CI, provenance, security/trust, minimal maintainer interaction, and release compatibility. Gate 1 and Gate 2 approvals do not transfer to the amendment: the checkpoint returns to crystallization for amended Gate 1 review, with Gate 2 invalidated. No model-backed test, workflow, code, remote setting, commit, tag, or publication is authorized or performed by this definition update.

## 2026-10-03 — Amended Gate 1 approved

The user replied "apruebo" to the pending amended Gate 1 after reviewing the main changes. This approves DN-005 / DN-006 behavior, R-11 through R-14, and the operating direction. Concept, requirements, and decisions are Approved. Gate 2, plan revision 3, implementation, model-backed runs, remote changes, and publication remain unapproved. Technical design now proceeds without another request to start it.

## 2026-10-03 — CI and readiness technical design ready for Gate 2

Resolved the previously deferred representation, policy ownership, interface compatibility, required-check names, retention, and failure behavior. Architecture, data model, and interfaces are Review. The proposed GitHub evidence adapter uses authenticated attempt-specific job/artifact metadata, safe bounded downloads, and exact candidate binding; the shared promotion policy consumes verified bytes and preserves existing local behavior. The additive CI-aware release-check options include explicit repository/run/attempt and previous-release SHA, plus optional separate behavioral evidence.

Use a new version-1 CI evidence document while preserving the existing report and promotion schemas. Request 30-day review retention, reject incomplete or mixed attempts, and stage successful outputs without overwriting user files. The previous-release ref is an ancestor with a lower version; optional behavioral results remain independent. Actual remote protection, artifact retention support, and hosted runner behavior are delivery acceptance evidence, not claims of current capability. No workflow, tooling, dependency, schema file, model call, or remote state was implemented or changed by this technical definition.

Credential-free verification passed: working-tree `devquitect check`, Ruff, and `git diff --check`. The consistency audit confirmed Gate 1 approved / Gate 2 pending, matching canonical statuses, preserved DN-001 through DN-004 inventory and delivery records, and compatibility of the proposed CI/readiness report entries with the existing report schema. Verification covers definition consistency and the current repository, not execution of the proposed hosted workflows.

## 2026-10-03 — Gate 2 approved

The user explicitly stated "apruebo gate 2". Architecture, evidence representation, additive release-check interfaces, and technical decisions are Approved. The remaining definition action is to finalize plan revision 3 with the approved paths, interfaces, validation, and evidence requirements, then obtain separate plan approval. This does not authorize DN-005 / DN-006 implementation, model-backed testing, remote changes, or publication.

## 2026-10-03 — Final plan revision 3 ready for approval

Finalized the existing revision-3 amendment from the approved technical design: DN-005 owns the CI evidence schema/producer and workflow contract test; DN-006 owns the GitHub evidence adapter, its unit fixtures, and compatible release-check extension. The plan specifies exact selectors and dispatch inputs, 30-day retention, safe bounded extraction, legacy behavior, separate behavioral row index, staged output, and policy/configuration/infrastructure exits. The requirement-to-slice/check mapping covers R-01 through R-14 with no unresolved implementation-blocking design choice.

The inventory audit passed for six matched slice headings/keys and 23 unique checks. DN-001 through DN-004, existing AC-DN-009 through AC-DN-012, and revision-2 delivery files remain unchanged. New-file checks target explicitly proposed delivery paths and are not represented as already executable. Plan revision 3 remains Review for separate approval; hosted evidence and remote settings remain future acceptance work. No implementation, model call, commit, or remote action was performed.

## 2026-10-03 — Plan revision 3 approved

The user explicitly stated "Apruebo el plan" in response to the pending plan-revision-3 approval. The plan is Approved and the definition workflow is complete with both gates approved. This records approval of the delivery definition only; it does not authorize DN-005 / DN-006 execution, behavioral tests, remote changes, commits, tags, or publication. Revision-2 delivery evidence remains untouched and requires explicit reconciliation during later authorized project-plan-execution.
