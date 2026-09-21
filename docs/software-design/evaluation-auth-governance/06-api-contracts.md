# Evaluation Authentication Governance contracts

Status: Approved
Last updated: 2026-09-21

## Confirmed

- The existing behavioral commands already accept model and reasoning configuration and write
  versioned reports.
- Authentication is currently passed internally as an optional cache path rather than a public,
  validated mode.

## Assumptions

- Exact flag spelling can change during implementation without changing the concepts below.
- Report schema evolution will use the repository's existing compatibility rules and will not include
  secrets or source credential paths.

## Open decisions

None. `chatgpt-cache-local` is local-only, explicit, and supervised.

## Proposed CLI contract

Behavioral commands (`eval`, `compare`, `calibrate`, and behavioral `check`) expose a common
authentication selection:

```text
--auth-mode credential-free | api-key | chatgpt-cache-local
--auth-cache PATH                 # valid only with chatgpt-cache-local
--allow-subscription-auth         # explicit acknowledgement for local cache mode
```

Rules:

- Structural `check` rejects behavioral-only auth flags unless `--behavioral` is also present.
- `credential-free` is the only default for non-behavioral commands.
- `api-key` requires the supported environment credential and never reads `auth.json`.
- `chatgpt-cache-local` requires `--auth-cache` or an equivalent explicit path; implicit
  `~/.codex/auth.json` discovery is removed.
- `--allow-subscription-auth` is mandatory for the local cache mode and never permits unattended
  use under the approved policy.
- Invalid combinations fail before snapshot execution or credential staging.

## Proposed report metadata

Add non-secret fields to evaluation/check evidence:

```json
{
  "authentication": {
    "mode": "api-key",
    "execution_context": "unattended-behavioral",
    "policy": "allowed",
    "credential_state": "injected",
    "cleanup": "not_applicable"
  }
}
```

Allowed values are defined by `03-domain.md`. A refused or failed run records the policy and
failure classification without a cache path, token, raw auth error, or credential contents.

## Internal adapter contract

The evaluator passes an explicit auth decision and credential source to both `run_codex` and
`run_app_server`. Adapters must not call user-home discovery. The source is either a validated
environment mapping or a validated file path owned by the current attempt policy. Staging returns a
cleanup handle/state, and cleanup is idempotent so setup failure cannot bypass it.

## Compatibility and migration

- Existing structural commands remain compatible and credential-free.
- Existing behavioral scripts that relied on automatic cache discovery receive a clear error naming
  the new explicit mode, not a silent fallback.
- Reports that predate authentication metadata remain readable; missing auth metadata is interpreted
  as `unknown` for historical evidence, never as `allowed`.
