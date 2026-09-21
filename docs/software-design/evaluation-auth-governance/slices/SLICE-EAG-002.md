---
schema_version: 1
session: evaluation-auth-governance
slice: SLICE-EAG-002
plan_revision: 2
plan_digest: 2ea060cc63793ac91246703a10b1a7e85ddd2c9995520fdebd3391f4b75a7972
verified_at: "2026-09-21T21:06:50.429912Z"
inputs_digest: 0c67fe13a63aab43e3e06258fc2c226ec933653a49c3166d0094d4aba0b49eb5
environment:
  python: "3.14.7"
  platform: Darwin
criteria:
  AC-EAG-005:
    action: "Exercise isolated credential staging for one attempt"
    expected: "Approved credentials remain isolated from workspace, evidence, and reports"
    method: "tests/unit/test_auth_lifecycle.py and tests/integration/test_fake_codex_run.py"
    observed: "The fake Codex run saw the credential only in the isolated CODEX_HOME; the staged file was absent afterward and no workspace/evidence/report path received it."
    status: PASS
    evidence: CHECK-EAG-002
  AC-EAG-006:
    action: "Exercise staged-file and source-file permission validation"
    expected: "Staged credentials are owner-only from creation and sources are regular non-symlink files"
    method: "tests/unit/test_auth_lifecycle.py"
    observed: "The lifecycle tests accepted only owned regular non-symlink 0600 sources and observed the destination at 0600 during creation."
    status: PASS
    evidence: CHECK-EAG-002
  AC-EAG-007:
    action: "Exercise handled cleanup across completion, timeout, malformed output, and child failure"
    expected: "No staged auth.json remains after handled lifecycle outcomes"
    method: "tests/unit/test_auth_lifecycle.py, tests/integration/test_fake_codex_run.py, and tests/integration/test_app_server_adapter.py"
    observed: "Normal completion, child exit 7, timeout, malformed Codex output, and App Server protocol failure all returned with no staged auth.json."
    status: PASS
    evidence: CHECK-EAG-002
  AC-EAG-008:
    action: "Exercise stale-attempt recovery boundaries"
    expected: "Only expired, tool-marked, owned, non-live attempt roots are removed"
    method: "tests/unit/test_auth_lifecycle.py"
    observed: "Only the expired marked root with a dead PID was removed; the live root, malformed marker, and source-cache file remained untouched."
    status: PASS
    evidence: CHECK-EAG-002
checks:
  CHECK-EAG-002:
    command: "uv run pytest tests/unit/test_auth_lifecycle.py tests/integration/test_fake_codex_run.py tests/integration/test_app_server_adapter.py -q"
    cwd: "."
    started_at: "2026-09-21T21:06:34.463877Z"
    finished_at: "2026-09-21T21:06:38.810030Z"
    exit_code: 0
    status: PASS
    observed: "9 passed in 3.88s."
    inputs_before: 0c67fe13a63aab43e3e06258fc2c226ec933653a49c3166d0094d4aba0b49eb5
    inputs_after: 0c67fe13a63aab43e3e06258fc2c226ec933653a49c3166d0094d4aba0b49eb5
---

# Evidence

The safe lifecycle implementation stages owner-only credentials per attempt, cleans handled
failures, and scavenges only expired, marked, owned, non-live attempt roots.
