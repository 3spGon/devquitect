---
schema_version: 1
session: evaluation-auth-governance
slice: SLICE-EAG-003
plan_revision: 2
plan_digest: 2ea060cc63793ac91246703a10b1a7e85ddd2c9995520fdebd3391f4b75a7972
verified_at: "2026-09-21T22:37:00.435750Z"
inputs_digest: faf458adfa767d5b9749154c5578db31d3e8368952fc4dd93a33d7e16f73f977
environment:
  python: "3.12.13"
  platform: Darwin
criteria:
  AC-EAG-009:
    action: "Exercise authentication metadata, refusal, cleanup, redaction, and legacy report handling"
    expected: "Reports are schema-valid, non-secret, diagnosable, and historical reports read as unknown"
    method: "tests/unit/test_reporting.py and tests/integration/test_check_command.py"
    observed: "Authentication metadata is emitted as credential-free/allowed/not-needed for structural check, successful behavioral reports carry bounded mode/context/policy/credential state/cleanup fields, policy refusal writes a non-passing report without the raw auth path or error, nested authentication runtime errors collapse to a safe diagnostic class, cleanup failures are classified as cleanup-failed, and missing historical metadata resolves to unknown."
    status: PASS
    evidence: CHECK-EAG-003
checks:
  CHECK-EAG-003:
    command: "uv run pytest tests/unit/test_reporting.py tests/integration/test_check_command.py -q"
    cwd: "."
    started_at: "2026-09-21T22:36:00Z"
    finished_at: "2026-09-21T22:36:45Z"
    exit_code: 0
    status: PASS
    observed: "17 passed in 45.10s."
    inputs_before: faf458adfa767d5b9749154c5578db31d3e8368952fc4dd93a33d7e16f73f977
    inputs_after: faf458adfa767d5b9749154c5578db31d3e8368952fc4dd93a33d7e16f73f977
---

# Evidence

PASS

Implementation files: `src/devquitect_quality/models.py`, `src/devquitect_quality/reporting.py`,
`src/devquitect_quality/cli.py`, `src/devquitect_quality/codex_adapter.py`,
`src/devquitect_quality/app_server_adapter.py`, `schemas/report.schema.json`, and
`schemas/calibration-report.schema.json`; tests cover report metadata, redaction, legacy unknown
handling, structural evidence, and unattended policy refusal.

Additional current verification:

- `uv run devquitect check --source working-tree --report .devquitect-reports/check.json` — exit 0;
  schema validation and fast credential-free suite passed.
- `uv run ruff check src tests` — exit 0.
- `git diff --check` — exit 0.
- `graphify update .` — code graph rebuilt successfully.

Residual risk: a forced parent termination may leave stale credential material until bounded stale
recovery; reports do not claim SIGKILL-proof cleanup.
