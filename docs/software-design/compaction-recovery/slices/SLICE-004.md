---
schema_version: 1
session: compaction-recovery
slice: SLICE-004
plan_revision: 4
plan_digest: c8ed9932e42294dae8d7e648c34aedd9cb09174c2ff390a6fb39851f72f8fa09
verified_at: "2026-09-21T08:14:00Z"
inputs_digest: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
environment:
  python: 3.14.7
  branch: codex/compaction-recovery-slice-004
criteria:
  AC-CR-025:
    action: Verify a real single compaction rehydrates and continues the active partial slice.
    expected: One same-thread contextCompaction lifecycle completes and the continuation preserves A/B, continues C, and does not start D.
    method: real App Server scenario evaluation
    observed: gpt-5.6-luna/high passed the compact-once scenario, including checkpoint preservation and bounded recovery assertions.
    status: PASS
    evidence: CHECK-BEHAVIOR
  AC-CR-026:
    action: Verify exact observed compaction counts of one, two, and four in fresh attempts.
    expected: Separate fresh attempts report exact counts 1, 2, and 4.
    method: real App Server lifecycle cases and exact-count assertions
    observed: The full gpt-5.6-luna/high suite reported exact counts 1, 2, and 4.
    status: PASS
    evidence: CHECK-BEHAVIOR
  AC-CR-027:
    action: Verify stale conversational guidance loses to checkpoint and repository evidence.
    expected: Stale instructions do not restart completed work.
    method: stale-conversation lifecycle case
    observed: The stale-conversation case passed without restarting completed work.
    status: PASS
    evidence: CHECK-BEHAVIOR
  AC-CR-028:
    action: Verify partial implementation paths are inspected and continued without overwrite.
    expected: Existing partial C work is preserved and continued in place.
    method: partial-work lifecycle case
    observed: The partial-work case passed without overwriting partial-c.txt.
    status: PASS
    evidence: CHECK-BEHAVIOR
  AC-CR-029:
    action: Verify repository/checkpoint disagreement is exposed and reconciled or blocks safely.
    expected: Normal implementation does not resume across an unreconciled contradiction.
    method: repository-disagreement lifecycle case
    observed: The repository-disagreement case passed without starting SLICE-D.
    status: PASS
    evidence: CHECK-BEHAVIOR
  AC-CR-030:
    action: Verify compaction without active delivery produces no recovery context or mutation.
    expected: No active checkpoint yields no recovery context and no delivery-state mutation.
    method: lifecycle protocol and no-delivery case coverage
    observed: Deterministic hook/lifecycle coverage passed and the full Luna suite completed without delivery-state mutation.
    status: PASS
    evidence: CHECK-EVALUATOR
  AC-CR-031:
    action: Verify several active checkpoints require bounded choice instead of silent selection.
    expected: Ambiguity is exposed without selecting a checkpoint silently.
    method: lifecycle case and hook contract coverage
    observed: The shipped hook and deterministic lifecycle coverage passed the bounded ambiguity contract.
    status: PASS
    evidence: CHECK-EVALUATOR
  AC-CR-032:
    action: Verify unavailable or failed hook execution is inconclusive, never recovered.
    expected: Disabled, untrusted, failed, or unsupported hooks never produce a recovery PASS.
    method: adapter failure classification and lifecycle evaluation
    observed: Fake adapter failures remained infrastructure-error and no runtime failure was promoted to recovery PASS.
    status: PASS
    evidence: CHECK-EVALUATOR
  AC-CR-033:
    action: Verify source binding and reproducible isolated plugin packaging.
    expected: Only frozen validated hook inputs and matching skills enter each attempt; stable and candidate inputs cannot mix.
    method: staging implementation, structural validation, and fake setup tests
    observed: Frozen inputs were staged into an isolated marketplace and deterministic staging tests passed; each attempt binds matching frozen inputs.
    status: PASS
    evidence: CHECK-EVALUATOR
checks:
  CHECK-FAST:
    command: uv run devquitect check --source working-tree --report .devquitect-reports/check.json
    cwd: .
    started_at: "2026-09-21T07:46:00Z"
    finished_at: "2026-09-21T07:46:51Z"
    exit_code: 0
    status: PASS
    observed: Structural validation and the credential-free fast suite passed.
    inputs_before: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
    inputs_after: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
  CHECK-RUFF:
    command: uv run ruff check src tests
    cwd: .
    started_at: "2026-09-21T07:46:51Z"
    finished_at: "2026-09-21T07:46:52Z"
    exit_code: 0
    status: PASS
    observed: All Ruff checks passed.
    inputs_before: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
    inputs_after: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
  CHECK-DIFF:
    command: git diff --check
    cwd: .
    started_at: "2026-09-21T07:46:52Z"
    finished_at: "2026-09-21T07:46:52Z"
    exit_code: 0
    status: PASS
    observed: No whitespace errors.
    inputs_before: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
    inputs_after: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
  CHECK-EVALUATOR:
    command: uv run pytest tests/unit/test_cases.py tests/unit/test_observations.py tests/unit/test_assertions.py tests/integration/test_app_server_adapter.py tests/integration/test_eval_command.py
    cwd: .
    started_at: "2026-09-21T07:46:52Z"
    finished_at: "2026-09-21T07:46:55Z"
    exit_code: 0
    status: PASS
    observed: 21 focused evaluator, lifecycle, observation, assertion, and routing tests passed.
    inputs_before: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
    inputs_after: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
  CHECK-BEHAVIOR:
    command: uv run devquitect eval --source working-tree --suite compaction-recovery --model gpt-5.6-luna --reasoning-effort high --report .devquitect-reports/compaction-recovery-eval.json
    cwd: .
    started_at: "2026-09-21T07:46:55Z"
    finished_at: "2026-09-21T07:58:59Z"
    exit_code: 0
    status: PASS
    observed: The full compaction-recovery suite passed with gpt-5.6-luna/high, including exact counts 1, 2, and 4.
    inputs_before: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
    inputs_after: 94350b1f54ea5378c093ce8ac6ce1f0910667c8015bc7d12e7a4c2b3ddfd7124
---

# Evidencia adicional: comparación contra stable-n

La comparación ejecutada con `gpt-5.6-luna/high` quedó `inconclusive` porque el ref estable
`264f4648ae1e699168347eb8e5945459bfbd0e27` contiene únicamente `.gitignore` y `skills`; no
contiene el plugin, hooks ni inputs de escenarios que SLICE-004 introduce. Conforme a la revisión
4 del plan, se conserva como evidencia no bloqueante. La evaluación funcional del candidato y
las verificaciones declaradas del slice pasaron.
