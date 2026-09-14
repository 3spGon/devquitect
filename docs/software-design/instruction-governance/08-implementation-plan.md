# Instruction Governance Implementation Plan

Status: Approved
Last updated: 2026-09-10
Plan revision: 1

## Goal

Implement lightweight authority validation, deterministic-only promotion, and optional versioned
behavior-calibration reports.

## Constraints

- Reuse the Python tooling under `src/devquitect_quality/` and existing JSON/YAML conventions.
- Do not make model-backed execution a promotion prerequisite.
- Keep calibration evidence outside packaged `skills/` and credential-free checks mandatory.

## Slices

### SLICE-001 — Authority map validation

Add the external authority-map schema and validation in `src/devquitect_quality/validate.py` with
focused tests in `tests/unit/test_validate.py`. Acceptance: unique IDs, safe existing owner paths,
and permitted secondary paths pass; malformed, missing, duplicate, or unsafe entries fail with
stable records. Verify with `uv run pytest tests/unit/test_validate.py` and credential-free check.

### SLICE-002 — Calibration report contract

Add the calibration report schema under `schemas/`, report construction in
`src/devquitect_quality/reporting.py`, and focused unit tests. Extend the CLI with an explicitly
invoked calibration command that retains bounded, redacted evidence. Acceptance: reports carry
snapshot, model/runtime, suite, repetitions, dimensions, optional score, and `unknown` absence;
compatible comparisons require matching configuration. Verify with focused reporting/CLI tests.

### SLICE-003 — Promotion separation and documentation

Update `src/devquitect_quality/promotion.py`, CLI tests, and contributor guidance so promotion
accepts deterministic evidence only and rejects calibration reports as eligibility evidence.
Acceptance: calibration never changes release eligibility; existing deterministic promotion and
package identity rules remain intact. Verify with promotion/release-check tests, full
credential-free check, Ruff, and diff check; refresh System Context after implementation passes.

## Traceability

REQ-IG-01–REQ-IG-05 map to SLICE-001; REQ-IG-08–REQ-IG-10 map to SLICE-002 and SLICE-003;
REQ-IG-06–REQ-IG-07 map to SLICE-003.

## Deferred

No automated promotion decision from calibration scores and no prose-contradiction linter.
