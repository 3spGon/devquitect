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

Canonical versioned records live in the [repository skill-change ledger](../../skill-change-ledger.md). This session indexes its rule groups without duplicating their evidence:

- [PC-DN-001-DEF — Definition workflow and authority boundary](../../skill-change-ledger.md#pc-dn-001-def--definition-workflow-and-authority-boundary)
- [PC-DN-001-DEL — Delivery authorization and verified close](../../skill-change-ledger.md#pc-dn-001-del--delivery-authorization-and-verified-close)
- [PC-DN-001-REF — Behavior-preserving refactor workflow](../../skill-change-ledger.md#pc-dn-001-ref--behavior-preserving-refactor-workflow)

The deterministic representative cases are unchanged. The original PC-DN-001 records preserve their pre-authorization `inconclusive` verdicts. The user later authorized [BC-DN-001-001](../../skill-change-ledger.md), which compared all nine cases and returned `equivalent`; reports remain diagnostic-only because the candidate was a working tree.
