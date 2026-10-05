# Devquitect Next interfaces and contracts

Status: Approved
Last updated: 2026-10-03

## Confirmed

### QUICK selection contract

`quick-change` is eligible only when the request is authorized, local, reversible, and directly verifiable. Its skill description states those triggers and exclusions. Explicit user invocation overrides ordinary implicit selection. Evidence of a material feature decision, public interface, persistence, security-sensitive behavior, migration, cross-module change, or durable-continuity need routes work away from QUICK.

### Existing verifier contract

The distributed verifier remains the current Python 3.12+ and PyYAML implementation over the fenced YAML inventory. This initiative preserves its commands, snapshot/check/atomic-close behavior, JSON stdout, and exit codes.

```text
python <skill-root>/scripts/verify_slice.py snapshot --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py check --session <directory> --slice <SLICE-ID>
python <skill-root>/scripts/verify_slice.py close --session <directory> --slice <SLICE-ID> --expected-revision <N>
```

It emits JSON on stdout and preserves exit codes: `0` valid operation, `1` evidence prevents acceptance, and `2` unsupported runtime, format, path, or revision condition.

### Prompt-change protocol contract

Before changing a prompt group, the maintainer records a baseline source identity, names the rules in scope, and selects the existing representative cases. The candidate changes one group in one skill. It must pass the same deterministic cases; an authorized behavioral comparison records one model/host configuration and is comparable only to evidence with matching configuration. A regression or inconclusive result retains the prior source and receives a ledger entry.

### Invocation and durable-root contract

`project-plan-execution` is explicit-only. Other skill metadata states its permitted implicit activation policy. Persistent workflow callers accept a configured root when supplied; otherwise they discover the repository default and previously recorded session roots. Ambiguous session discovery requires user selection rather than a silent choice.

The configured root is a single repository-relative path supplied by the caller; it is persisted as `definition_root` in `00-status.md`. The default is `docs/software-design`. A resumed session uses its recorded root first. Existing sessions without `definition_root` stay at their current path and are not migrated. Every session also records `workflow_depth` as `lightweight`, `standard`, or `rigorous`; an absent legacy value means `standard`.

### Evaluation-matrix contract

Each behavioral comparison is opt-in and separately authorized. One evidence row records one canonical model ID, host, runtime, reasoning effort where supported, case-suite revision, repetitions, and report references. The initial model IDs are `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`; the GPT-5.6 rows form the baseline and the GPT-6 rows are additional. Use the same prompt-change group and representative cases across rows. Use `high` reasoning effort where supported; if effort, host, or runtime differs, retain the value as part of that row's identity and do not present it as a model-only comparison. Verdicts remain independent; any release decision cites the rows that support it without combining their scores.

## Assumptions

The existing verifier contract remains adequate for the present initiative because it is explicitly out of scope.

## Approved DN-005 / DN-006 interfaces

The current, verified repository commands are:

```text
uv sync --locked --all-groups
uv run devquitect check --source HEAD --report .devquitect-reports/check.json
uv run ruff check src tests
uv run pytest tests/unit/test_compaction_recovery_hook.py tests/contract tests/unit/test_packaging.py
uv run devquitect package --source <candidate-sha> --version <version> --output <directory> --report <report-path>
uv run devquitect release-check --source <candidate-sha> --version <version> --evidence <directory> --output <directory> --report <report-path>
```

Angle-bracket values above are parameter explanations, not executable inventory commands. CI must install and test the same checkout it identifies as its source. `check` runs tests from the checkout even when structural validation selects a Git ref; a different installed revision would invalidate the clean-candidate claim.

The proposed manual readiness interface accepts a full candidate SHA, requested version, CI run ID and attempt, and an immutable previous-release reference. It must resolve and verify repository/workflow identity and all mandatory job conclusions, then download only the selected artifacts into a fresh namespace. Branch aliases, ambiguous attempts, unrelated SHA evidence, missing/expired files, invalid digests, and version mismatch cannot produce eligibility.

The existing `release-check` CLI has no input for a CI ZIP or manifest and uses the candidate parent as its compatibility baseline. Extend that command rather than add a second release manager. The following names and behavior are proposed interfaces for implementation after approval; they are not available commands yet:

| New option | Contract |
| --- | --- |
| `--previous-release <full-sha>` | Resolve the committed prior plugin version as the compatibility baseline; the reference must exist in this repository and precede the candidate in Git ancestry, and candidate version must increase. Optional in legacy local mode, mandatory in CI-aware mode. Omission preserves immediate-parent behavior. |
| `--repository <owner/repo>` | Expected GitHub repository; must agree with the checked-out remote and selected run. Never inferred from an evidence file. |
| `--ci-run-id <positive-integer>` | Explicit run of `.github/workflows/ci.yml`; initially require push on main and exact candidate SHA. |
| `--ci-run-attempt <positive-integer>` | Explicit complete attempt; partial reruns or mixed attempts cannot satisfy mandatory evidence. |
| `--behavioral-evidence <directory>` | Optional separate canonical model-backed reports, with authorization/dimensions and exact candidate binding; consume only, never launch a model. |

The three CI-selection options must appear together and require `--previous-release`; invalid combinations exit `2`. CI-aware mode requires `--source` to be a full SHA and uses read-only `GH_TOKEN` through the GitHub adapter. Existing `--evidence` must be a fresh empty directory in this mode; the adapter populates it only with selected verified deterministic evidence, avoiding stale local reports. CI-aware `--output` must not already exist: stage its output directory privately and rename it after successful validation/output generation, preserving existing user files. Existing local mode retains its populated-evidence-directory and output behavior and invokes no GitHub access when CI options are absent. `--behavioral-evidence` is supported only in CI-aware mode and kept outside mandatory deterministic evidence.

The adapter resolves exact jobs/artifacts, downloads the canonical ZIP/manifest itself, and passes verified paths plus observed provenance to shared promotion policy. Caller-supplied artifact URLs or a purported trusted metadata JSON are not accepted. The policy hashes the actual files, compares them with reproducible rebuilds and committed version/source, and validates all required conclusions before saving eligible outputs. Unit fixtures can replace the transport during testing; production cannot disable provenance checks through a user option.

An optional behavioral directory contains `rows.json` listing the R-10 dimensions, authorization references, independent verdicts, and safe relative canonical report paths with SHA-256 values. Validate those report schemas and candidate identities; reject undeclared/missing/mismatched reports. `not-run` rows have no report paths or observed runtime values. This is a supplementary row index over existing evidence, not a new evaluator or a trusted source of CI success.

CI-aware reports retain `report_type: release-check` and schema version 1. Exit `0` means deterministic eligibility and an unapproved proposal; `1` means policy rejection; `2` means malformed/unsupported configuration; `3` means infrastructure or unavailable verification. All failures have a non-passing canonical report with a diagnostic code; missing/expired required artifacts are policy rejection, while API access/service failure is unavailable verification. Existing legacy exit/output behavior remains unchanged. In CI-aware mode the ZIP, package manifest, and proposal are finalized only after all checks, with reports written atomically; a failure leaves no eligible output/proposal.

`release-readiness.yml` dispatch inputs are `candidate_sha`, `version`, `ci_run_id`, `ci_run_attempt`, and `previous_release_sha`. The repository is its fixed `github.repository`, not a cross-repository input. Optional authorized behavioral files may be staged separately by the maintainer; an absent input records `not-run`. The workflow checks out the reviewed candidate and calls the above interface, with token values passed through environment variables rather than command text, reports, or logs.

The readiness report must distinguish successful eligibility from policy failure, malformed inputs, infrastructure/unavailable evidence, and optional behavioral `inconclusive` / `not-run`. It never calls a model and never grants publication authority. The behavioral workflow is manual and separate; DN-004 controls its matrix, API-key configuration is explicit, and local supervised subscription caches are not supported on unattended CI.

`behavioral.yml` accepts a reviewed repository `candidate_sha`, one DN-004 `model_id`, suite/repetitions, and an authorization reference. Its dedicated manual job uses the existing `--auth-mode api-key` interface, records actual host/runtime/effort, and defaults to the repository's gpt-5.6-luna / high calibration unless an authorized matrix row specifies otherwise. Missing authorization or API configuration records non-run with a clear reason; authentication/service failures remain inconclusive. No secrets are exposed to normal PR jobs and no dispatch is performed during definition work.

PR whitespace checks must compare the tested commit against the event's actual base SHA, rather than hardcode `origin/main`. A `push` check uses its valid before/after range, with a documented first-push fallback. A merge queue, if enabled, requires a `merge_group` trigger. Required-check names must be unique and stable; an aggregate matrix gate must run after failure and explicitly reject failed, cancelled, missing, or skipped mandatory variants.

## Open decisions

None. The user approved these additive interfaces at Gate 2 on 2026-10-03. They remain proposed implementation, not available CLI options until delivery. The established skill, verifier, ledger, invocation, and model-matrix contracts remain unchanged.
