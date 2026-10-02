# Devquitect prompt-change ledger

Status: Review
Last updated: 2026-09-24

## Purpose

This append-only ledger makes each staged prompt simplification reviewable without copying source text. Immutable source snapshots and Git references reconstruct the original and candidate; comparison and calibration reports remain the evidence source.

## Entry template

### PC-<ID> — <rule group>

- **Baseline:** `<source snapshot ID or Git reference>`
- **Candidate:** `<source snapshot ID or Git reference>`
- **Scope:** `<skill path and named rule group>`
- **Disposition:** retain | move | remove
- **Deterministic cases:** `<case IDs and result>`
- **Behavioral configuration:** `<model, host, runtime, suite version, repetitions, or not authorized>`
- **Evidence:** `<comparison or calibration report references>`
- **Verdict:** retained | reverted | inconclusive
- **Rationale:** `<brief evidence-based explanation>`

## Entries

### BC-DN-004-001 — Authorized v0.8.0 follow-up

On 2026-10-02 the user authorized v0.8.0 preparation and relevant model comparisons.
The append-only [observed rows](../../skill-change-ledger.md#bc-dn-004-001--authorized-v080-comparison-follow-up)
retain the same source pair, twelve cases, and suite revision. Both rows use gpt-5.6-luna/high
but differ in the supervisor sandbox, so their results remain separate. The restricted row
has four shared functional failures; the corrected row passes all twelve candidate cases,
with ten equivalent pairs and two matrix improvements. All credential cleanup passed.
The [release review](../../releases/v0.8.0.md) records package and promotion provenance.

### PC-DN-004 — Invocation policies and independent evaluation rows

The user authorized SLICE-DN-004 implementation on 2026-10-02, without behavioral comparisons.
The immutable baseline is `git:dff146543c870a56b55d1ed339eeb95f6397653f`.
[PC-DN-004 records](../../skill-change-ledger.md#pc-dn-004-del--explicit-only-delivery-invocation)
separate the delivery metadata, definition metadata, and evidence-matrix rule groups, record each
candidate file hash, and retain the positive/negative cases. The matrix inventory fixes twelve
representative cases at suite revision
`sha256:e6f14a59da173317677421a4d43456d58541e4fdbf8d79e148be7b7d044804d0`.
Its five independent model rows are unexecuted (`not-run`); no host/runtime observations or
comparison reports are fabricated. Current deterministic and repository evidence belongs in
`slices/SLICE-DN-004.md`; behavioral verdicts remain inconclusive until separately authorized.

Canonical versioned records live in the [repository skill-change ledger](../../skill-change-ledger.md). This session indexes its rule groups without duplicating their evidence:

- [PC-DN-001-DEF — Definition workflow and authority boundary](../../skill-change-ledger.md#pc-dn-001-def--definition-workflow-and-authority-boundary)
- [PC-DN-001-DEL — Delivery authorization and verified close](../../skill-change-ledger.md#pc-dn-001-del--delivery-authorization-and-verified-close)
- [PC-DN-001-REF — Behavior-preserving refactor workflow](../../skill-change-ledger.md#pc-dn-001-ref--behavior-preserving-refactor-workflow)
- [PC-DN-003-WFD — Common workflow depth](../../skill-change-ledger.md#pc-dn-003-wfd--common-workflow-depth)
- [PC-DN-003-ROOT — Persistent definition-root continuity](../../skill-change-ledger.md#pc-dn-003-root--persistent-definition-root-continuity)
- [PC-DN-003-ART — Artifact directory follows the durable root](../../skill-change-ledger.md#pc-dn-003-art--artifact-directory-follows-the-durable-root)

The deterministic representative cases are unchanged. The original PC-DN-001 records preserve their pre-authorization `inconclusive` verdicts. The user later authorized [BC-DN-001-001](../../skill-change-ledger.md), which compared all nine cases and returned `equivalent`; reports remain diagnostic-only because the candidate was a working tree.
