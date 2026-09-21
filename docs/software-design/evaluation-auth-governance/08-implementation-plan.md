# Evaluation Authentication Governance implementation plan

Status: Approved
Last updated: 2026-09-21
Plan revision: 2

## Goal

Make behavioral evaluation authentication explicit, local-subscription use supervised-only, and
credential cleanup auditable without changing the credential-free structural quality path.

## Approved design inputs

- [01-concept.md](01-concept.md)
- [02-requirements.md](02-requirements.md)
- [03-domain.md](03-domain.md)
- [04-architecture.md](04-architecture.md)
- [06-api-contracts.md](06-api-contracts.md)
- [07-decisions.md](07-decisions.md)
- The user-approved boundary from 2026-09-21: `chatgpt-cache-local` is explicit, local, and
  supervised only; it is not valid for CI, cron, schedulers, daemons, automatic retries, recurring
  loops, promotion, or publication.

## Global constraints and non-goals

- Preserve the credential-free default for structural checks.
- Preserve model/reasoning configurability, sandbox restrictions, report exit semantics, and case
  behavior unless the approved requirements explicitly add auth metadata or refusal behavior.
- Do not add a provider plugin framework, hosted credential broker, secret manager, or CI service.
- Do not claim deletion after `SIGKILL`; provide only deterministic handled cleanup and bounded stale
  recovery.
- Do not run real model-backed evaluations as part of implementation verification unless separately
  authorized.

## Repository context

The verified implementation seams are `src/devquitect_quality/cli.py`, `evaluation.py`,
`codex_adapter.py`, `app_server_adapter.py`, `reporting.py`, `schemas/report.schema.json`, and the
existing unit/integration tests under `tests/`. Existing verification uses `uv run pytest`,
`uv run devquitect check`, `uv run ruff check src tests`, and `git diff --check`.

## Delivery slices

### SLICE-EAG-001 — Explicit authentication policy boundary

Outcome: behavioral commands select authentication explicitly and never autodiscover
`~/.codex/auth.json`.

Acceptance criteria:

- `check` without behavioral execution never reads, copies, or references a login cache.
- `--auth-mode` validation rejects missing credentials, invalid combinations, and local cache use
  without explicit acknowledgement before Codex starts.
- `api-key` uses only the approved environment boundary; `chatgpt-cache-local` requires an explicit
  source and remains local/supervised-only.
- Existing `--model` and `--reasoning-effort` behavior remains independent of auth selection.
- Behavioral callers that relied on implicit discovery receive a migration error rather than a silent
  fallback.

Files and interfaces:

- Modify verified paths: `src/devquitect_quality/cli.py`, `src/devquitect_quality/evaluation.py`,
  `src/devquitect_quality/codex_adapter.py`, `src/devquitect_quality/app_server_adapter.py`.
- Proposed path: `src/devquitect_quality/auth_policy.py`, only if the policy boundary cannot remain
  small and testable in existing modules.
- Add or modify tests: `tests/unit/test_auth_policy.py` (proposed),
  `tests/unit/test_codex_adapter.py`, `tests/integration/test_eval_command.py`, and
  `tests/integration/test_check_command.py`.

Dependencies: none.

Verification: policy unit tests plus the existing evaluation and check integration tests; all must
pass without credentials and must prove that structural check does not touch the cache.

Rollback and compatibility: revert the explicit policy boundary as one change; preserve the
credential-free path. Do not restore implicit cache discovery.

### SLICE-EAG-002 — Safe credential lifecycle and stale recovery

Outcome: approved credentials are isolated per attempt, created with restrictive permissions, cleaned
up for handled failures, and recoverable after an abrupt parent termination without deleting user data.

Acceptance criteria:

- Staged files are created owner-only from creation and source files are regular, non-symlink files
  with acceptable permissions.
- Setup failure after file creation cannot bypass cleanup.
- Child non-zero exit, timeout, malformed output, and normal completion remove staged credentials.
- Tool-owned markers, age bounds, ownership checks, and liveness checks restrict stale cleanup to
  expired attempt roots; active or ambiguous roots remain untouched.
- Documentation and reports make no SIGKILL-proof deletion claim.

Files and interfaces:

- Modify verified paths: `src/devquitect_quality/codex_adapter.py`,
  `src/devquitect_quality/app_server_adapter.py`, and `src/devquitect_quality/fixtures.py` only if
  attempt markers must be owned there.
- Add or modify tests: proposed `tests/unit/test_auth_lifecycle.py`,
  `tests/integration/test_fake_codex_run.py`, and `tests/integration/test_app_server_adapter.py`.

Dependencies: `SLICE-EAG-001`.

Verification: lifecycle unit tests, fake Codex failure tests, App Server lifecycle tests, and the
credential-free check. Tests must inspect only test-owned temporary paths and must never touch the
user's real `~/.codex`.

Rollback and compatibility: disable stale scavenging independently if it proves unsafe; retain
handled cleanup and explicit mode validation. Never broaden deletion scope to recover a failure.

### SLICE-EAG-003 — Non-secret evidence and report compatibility

Outcome: reports explain auth policy and cleanup outcomes without retaining credentials, while old
reports remain readable.

Acceptance criteria:

- Reports record auth mode, execution context, policy decision, credential state, and cleanup class.
- Reports never include cache contents, tokens, raw credential paths, or unredacted auth errors.
- Historical reports missing auth metadata remain readable as `unknown`, never implicitly `allowed`.
- Policy refusal and cleanup failure are non-passing, diagnosable outcomes.

Files and interfaces:

- Modify verified paths: `src/devquitect_quality/reporting.py`, `src/devquitect_quality/models.py`,
  `schemas/report.schema.json`, and `src/devquitect_quality/cli.py`.
- Add or modify tests: `tests/unit/test_reporting.py`, `tests/integration/test_check_command.py`,
  and a proposed report/auth integration case.

Dependencies: `SLICE-EAG-001`, `SLICE-EAG-002`.

Verification: report unit tests, integration report assertions, structural `devquitect check`, and
Ruff. Expected signal is exit code `0` with schema-valid reports and no secret-bearing fields.

Rollback and compatibility: schema additions are optional/defaultable for old reports; revert only
the new metadata fields if compatibility evidence fails, without reintroducing secret capture.

### SLICE-EAG-004 — Migration documentation and verified baseline refresh

Outcome: contributors understand the explicit auth contract, and the shared System Context reflects
the new behavior only after the implementation is verified.

Acceptance criteria:

- Contributor documentation states that local subscription auth is supervised-only and gives the
  refusal behavior for unattended contexts.
- Migration guidance replaces implicit cache discovery with explicit mode selection.
- The System Context refresh records the implemented baseline, affected capabilities, and verification
  evidence after slices 001–003 pass; it does not describe planned behavior prematurely.
- Rollback guidance and residual risks are documented.

Files and interfaces:

- Modify verified paths: `docs/contributing-skills.md` and, after implementation verification,
  `docs/software-design/system-context.md`.
- Add or modify documentation-focused assertions only where existing structural validation supports
  them; do not create a standalone documentation test suite.

Dependencies: `SLICE-EAG-001`, `SLICE-EAG-002`, `SLICE-EAG-003`.

Verification: full credential-free check, Ruff, `git diff --check`, and review of the final report
and System Context baseline reference.

Rollback and compatibility: revert documentation and implementation together if the explicit auth
contract cannot be supported; preserve the previous structural check behavior.

## Machine-readable verification inventory

```devquitect-verification
schema_version: 1
slices:
  SLICE-EAG-001:
    depends_on: []
    criteria:
      AC-EAG-001:
        text: "La ejecución estructural permanece libre de credenciales y no toca el cache de login."
        requirement: REQ-EAG-001
      AC-EAG-002:
        text: "La autenticación behavioral es explícita y rechaza credenciales faltantes o combinaciones inválidas antes de ejecutar Codex."
        requirement: REQ-EAG-002
      AC-EAG-003:
        text: "La autenticación por suscripción local exige intención explícita y es rechazada en ejecución unattended."
        requirement: REQ-EAG-003
      AC-EAG-004:
        text: "La selección de modelo y reasoning permanece independiente de la selección de autenticación."
        requirement: REQ-EAG-009
    inputs:
      - src/devquitect_quality/cli.py
      - src/devquitect_quality/evaluation.py
      - src/devquitect_quality/codex_adapter.py
      - src/devquitect_quality/app_server_adapter.py
      - src/devquitect_quality/auth_policy.py
      - tests/unit/test_auth_policy.py
      - tests/unit/test_codex_adapter.py
      - tests/integration/test_eval_command.py
      - tests/integration/test_check_command.py
    checks:
      CHECK-EAG-001:
        command: "uv run pytest tests/unit/test_auth_policy.py tests/unit/test_codex_adapter.py tests/integration/test_eval_command.py tests/integration/test_check_command.py -q"
        cwd: "."
  SLICE-EAG-002:
    depends_on:
      - SLICE-EAG-001
    criteria:
      AC-EAG-005:
        text: "Las credenciales aprobadas permanecen aisladas por intento y no contaminan workspace, evidencia ni reportes."
        requirement: REQ-EAG-004
      AC-EAG-006:
        text: "Los archivos staged se crean con permisos owner-only y las fuentes se validan como archivos regulares no simbólicos."
        requirement: REQ-EAG-005
      AC-EAG-007:
        text: "La limpieza determinista cubre completado, timeout, fallos manejados y salida fallida del hijo."
        requirement: REQ-EAG-006
      AC-EAG-008:
        text: "La recuperación stale queda limitada por markers, antigüedad, ownership y liveness, sin borrar raíces activas o ambiguas."
        requirement: REQ-EAG-007
    inputs:
      - src/devquitect_quality/codex_adapter.py
      - src/devquitect_quality/app_server_adapter.py
      - src/devquitect_quality/fixtures.py
      - tests/integration/test_fake_codex_run.py
      - tests/integration/test_app_server_adapter.py
    checks:
      CHECK-EAG-002:
        command: "uv run pytest tests/unit/test_auth_lifecycle.py tests/integration/test_fake_codex_run.py tests/integration/test_app_server_adapter.py -q"
        cwd: "."
  SLICE-EAG-003:
    depends_on:
      - SLICE-EAG-001
      - SLICE-EAG-002
    criteria:
      AC-EAG-009:
        text: "La evidencia de autenticación es auditable y no contiene secretos, tokens, rutas raw ni errores sin redacción."
        requirement: REQ-EAG-008
    inputs:
      - src/devquitect_quality/reporting.py
      - src/devquitect_quality/models.py
      - schemas/report.schema.json
      - tests/unit/test_reporting.py
    checks:
      CHECK-EAG-003:
        command: "uv run pytest tests/unit/test_reporting.py tests/integration/test_check_command.py -q"
        cwd: "."
  SLICE-EAG-004:
    depends_on:
      - SLICE-EAG-001
      - SLICE-EAG-002
      - SLICE-EAG-003
    criteria:
      AC-EAG-010:
        text: "La documentación declara la frontera supervised-only de la suscripción local."
        requirement: PLAN-EAG-004-DOC
      AC-EAG-011:
        text: "El System Context se refresca únicamente después de verificar la implementación."
        requirement: PLAN-EAG-004-CONTEXT
    inputs:
      - docs/contributing-skills.md
      - docs/software-design/system-context.md
      - .devquitect-reports/check.json
    checks:
      CHECK-EAG-004:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-EAG-005:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-EAG-006:
        command: "git diff --check"
        cwd: "."
```

## Residual risk and deferred work

- A forcibly killed parent can leave an encrypted or plaintext temporary artifact until stale
  recovery or operator cleanup; stronger guarantees require an external supervisor or an ephemeral
  filesystem and are deferred.
- External terms may change; policy documentation must be reviewed before enabling new execution
  contexts.
- No implementation slice is authorized by this plan. Execution requires explicit user authorization
  with a concrete slice list and then handoff to `$project-plan-execution`.
