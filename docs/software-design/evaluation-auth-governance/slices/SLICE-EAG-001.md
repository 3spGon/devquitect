---
schema_version: 1
session: evaluation-auth-governance
slice: SLICE-EAG-001
plan_revision: 2
plan_digest: 2ea060cc63793ac91246703a10b1a7e85ddd2c9995520fdebd3391f4b75a7972
verified_at: "2026-09-21T20:25:53.678981Z"
inputs_digest: 858e827bbbbb6fe1bbfcc2eded29e420353b68caeecac8a50ed980e129f40f98
environment:
  python: "3.12.13"
  platform: Darwin
criteria:
  AC-EAG-001:
    action: "Run structural check with a login-cache file present"
    expected: "Structural execution remains credential-free and does not use the login cache"
    method: "tests/integration/test_check_command.py::test_structural_check_does_not_need_a_login_cache"
    observed: "The structural check passed with an invalid auth.json present under CODEX_HOME and did not invoke behavioral authentication."
    status: PASS
    evidence: CHECK-EAG-001
  AC-EAG-002:
    action: "Exercise behavioral authentication validation"
    expected: "Missing auth mode, missing API credentials, and invalid local-cache combinations fail before Codex starts"
    method: "tests/unit/test_auth_policy.py and tests/integration/test_check_command.py::test_behavioral_eval_without_auth_mode_returns_migration_error"
    observed: "Policy tests passed for explicit mode selection, API-key requirements, missing cache source, acknowledgement, structural combinations, and migration error."
    status: PASS
    evidence: CHECK-EAG-001
  AC-EAG-003:
    action: "Exercise subscription-cache execution policy"
    expected: "Local subscription cache requires explicit acknowledgement and is refused for unattended execution"
    method: "tests/unit/test_auth_policy.py::test_local_cache_requires_supervised_acknowledgement and tests/unit/test_auth_policy.py::test_local_cache_is_refused_for_unattended_behavior"
    observed: "Both supervised acknowledgement and unattended refusal cases passed without staging credentials or launching Codex."
    status: PASS
    evidence: CHECK-EAG-001
  AC-EAG-004:
    action: "Exercise model and reasoning overrides"
    expected: "Model and reasoning configuration remains independent of authentication selection"
    method: "tests/unit/test_codex_adapter.py::test_behavioral_command_allows_explicit_calibration_override"
    observed: "The adapter retained explicit gpt-5.6-terra and medium settings while auth policy remained a separate selection."
    status: PASS
    evidence: CHECK-EAG-001
checks:
  CHECK-EAG-001:
    command: "uv run pytest tests/unit/test_auth_policy.py tests/unit/test_codex_adapter.py tests/integration/test_eval_command.py tests/integration/test_check_command.py -q"
    cwd: "."
    started_at: "2026-09-21T20:25:00.448355Z"
    finished_at: "2026-09-21T20:25:53.678981Z"
    exit_code: 0
    status: PASS
    observed: "16 passed in 42.39s."
    inputs_before: 858e827bbbbb6fe1bbfcc2eded29e420353b68caeecac8a50ed980e129f40f98
    inputs_after: 858e827bbbbb6fe1bbfcc2eded29e420353b68caeecac8a50ed980e129f40f98
---

# Evidence

The implementation removes implicit login-cache discovery, validates explicit authentication
selection before behavioral execution, and preserves model/reasoning overrides.
