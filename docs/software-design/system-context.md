---
schema_version: 1
document: system-context
system: Devquitect
scope: repository
lifecycle: in-development
context_status: current
revision: 16
last_updated: 2026-10-05
baseline_reference: 1fb3c2f9a42cfb1861ab058fb257b1d1447e1930
---

# Devquitect system context

## Quick orientation

Devquitect is a Git repository containing three related Codex skills that cover software definition, approved plan execution, and targeted behavior-preserving refactoring. Repository-owned Python tooling freezes skills into isolated snapshots, validates their structure offline, and runs versioned behavioral cases through an isolated Codex CLI adapter.

## Purpose

The current system provides reusable agent workflows for moving from a software idea or change request to an approved technical definition, executing an explicitly authorized persistent plan, and performing narrowly scoped refactors without changing intended behavior.

## Current lifecycle

The repository is in development. A preliminary `v0.1.0` tag exists, and the `devquitec-architecture-definition` candidate carries the `0.4.0` plugin manifest, the verified local quality workflow, and the credential-free-verified proportional Change Profile workflow. The candidate is not promoted, tagged, published, or installed by this repository workflow. The skill set and its shared workflow contracts continue to evolve.

## System boundaries

Inside the current system:

- skill instructions under `skills/*/SKILL.md`;
- supporting workflow references under each skill's `references/` directory;
- optional Codex presentation and invocation metadata under `agents/openai.yaml`.
- Python source-snapshot records and materialization under `src/devquitect_quality/`;
- the stable N provenance manifest under `baselines/stable-n.json`;
- the Python toolchain and focused snapshot tests declared by `pyproject.toml` and `uv.lock`;
- the `devquitect` plugin definition under `.codex-plugin/plugin.json`;
- versioned validation schemas under `schemas/`, contributor guidance under `docs/`, and the
  isolated App Server lifecycle adapter for versioned compaction scenarios.
- hosted credential-free CI and effective protected PR merge gates on `main`.

Outside the current implemented baseline:

- public plugin distribution;
- automated release publication;
- MCP servers, connectors, applications, or graphical interfaces.

## Actors and external systems

- Skill maintainers and contributors author and review the repository content.
- Codex loads and follows the skill instructions when a request explicitly or implicitly selects them.
- Git records the source history and the `v0.1.0` preliminary release marker.

The configured Git remote is `git@github.com:3spGon/devquitect.git`. GitHub Actions is enabled;
actual DN-005 artifacts retain 30 days (repository configured/maximum: 90 days). Under the user's
2026-10-04 authorization, `main` now requires strict quality/platform aggregate/package success
from GitHub Actions app 15368 and PR integration, including administrators; force push and branch
deletion are disabled. PR 3 integrated only after all mandatory jobs passed.

## Current capabilities

- `project-plan-execution` distributes a deterministic `snapshot`/`check`/`close` guard that fingerprints approved inputs, validates slice evidence, and atomically protects the supported transition to `verified` without executing evidence commands; its execution loop now requires this verification before advancing or completing an authorized slice.
- `software-idea-to-project` defines new systems and software changes through approval gates and can preserve cross-session state in a target repository. Existing-system and hybrid initiatives use an optional Change Profile to select expedited, standard, or full depth from baseline evidence, with fail-safe elevation and backward-compatible schema-v2 persistence.
- `project-plan-execution` executes authorized slices from an approved persistent plan and records current verification evidence.
- `targeted-refactoring` assesses, plans, executes, or reviews bounded behavior-preserving refactors.
- The skills use progressive disclosure through directly referenced Markdown files.
- Each skill includes user-facing metadata in `agents/openai.yaml`.
- Stable N is identified by commit `264f4648ae1e699168347eb8e5945459bfbd0e27` and aggregate snapshot digest `sha256:062d5509956e73de366b9c351bb93441dcd39e2bf04cc8b6b870f797717960ef`.
- Git refs and working-tree skill sources can be copied into separate read-only snapshots with normalized file, skill, and aggregate SHA-256 identities.
- Git-ref snapshots are eligible stable sources; working-tree snapshots are always diagnostic-only, even when their skill files are clean.
- `devquitect validate --source <selector>` checks frontmatter, name consistency and uniqueness, local references, presentation metadata, schema compatibility, plugin membership, and package allowlists without credentials or network access.
- Validation also checks the external authority map for unique critical-contract IDs, safe existing owners, and permitted secondary roles.
- Validation emits the approved JSON report envelope, an equivalent text presentation, normalized relative paths, atomic report files, and stable exit codes `0`, `1`, and `2`.
- `devquitect eval` loads schema-valid YAML cases, creates a fresh Git workspace, conversation, Codex home, skill root, and evidence namespace per attempt, and emits canonical evaluation reports.
- Scenario cases drive Codex App Server over bounded stdio JSONL, stage a one-entry local
  marketplace from frozen validated inputs, and require same-thread `contextCompaction` lifecycle
  evidence; ordinary `turns` cases retain the `codex exec` path.
- Normalized observations retain bounded compaction lifecycle events and deterministic assertions
  can count completed compaction identities without counting the started/completed pair twice.
- Deterministic assertions dominate optional semantic grades; critical failures cannot be overridden and infrastructure failures remain inconclusive with exit `3`.
- Behavioral authentication is explicit: credential-free structural checks do not inspect a login cache, API-key runs use the supported environment boundary, and `chatgpt-cache-local` requires an explicit cache path plus acknowledgement for a supervised local run.
- Unattended, recurring, promotion, and publication contexts refuse `chatgpt-cache-local` before credential staging or Codex launch; the refusal is `chatgpt-cache-local is supervised-only and cannot run unattended`.
- `devquitect compare` freezes stable and candidate sources before execution, runs them independently, and classifies equivalent behavior, improvement, regression, reviewed contract change, variability, or inconclusive infrastructure.
- `devquitect calibrate` writes bounded, redacted, versioned behavior-calibration evidence for review; absent reports are unknown and only matching model, runtime, suite, and repetition configurations are comparable.
- `devquitect package` reads an exact Git commit, enforces the committed semantic version and package allowlist, and emits a normalized plugin ZIP with entry and artifact SHA-256 identities.
- `devquitect release-check` rebuilds in two fresh roots, requires a passing credential-free check bound to the same snapshot, ignores model-backed evidence for promotion eligibility, applies compatibility and migration policy, and emits an explicitly unapproved promotion proposal.
- `devquitect check` composes structural validation with the credential-free unit, integration, and CLI contract suite; `--behavioral` explicitly adds trusted critical evaluation and clean-ref self-hosting comparison.
- Real behavioral commands default to Codex CLI `gpt-5.6-luna` at `high` reasoning effort as a convenience, retain runtime identity in evidence, and allow explicit model and effort overrides; fast checks invoke no model.

## Evaluation Authentication Governance baseline

The implemented baseline after verified slices `SLICE-EAG-001` through `SLICE-EAG-003`, and this
documentation refresh, keeps the credential-free structural path unchanged while affecting the
behavioral command boundary, local credential staging, non-secret report metadata, contributor
migration guidance, and the shared context record. Behavioral callers select `credential-free`,
`api-key`, or `chatgpt-cache-local` explicitly; implicit `~/.codex/auth.json` discovery is not part
of the baseline. Local subscription authentication remains supervised-only and is refused in
unattended contexts before staging.

Verification evidence for this baseline is the current `.devquitect-reports/check.json` produced by
`uv run devquitect check --source working-tree --report .devquitect-reports/check.json`, together
with `uv run ruff check src tests` and `git diff --check`; the credential-free check passed with
exit code `0` and no behavioral/model-backed evaluation was run. Rollback is to revert the
documentation and explicit-auth implementation together while retaining the previous structural
check behavior. A forcibly killed parent can leave temporary material until bounded stale recovery
or operator cleanup; the baseline makes no SIGKILL-proof deletion claim.

## DN-005 continuous verification

The verified implementation defines `ci.yml` for pull requests and final `main` pushes, with
quality, three separately named platform jobs and an always-run aggregate, and canonical Linux
packaging. Normal jobs have `contents: read`, pinned actions/uv/Codex CLI, Python 3.12 and the
locked environment; they receive no model credentials. The existing HEAD credential-free check,
Ruff, and event-specific introduced-whitespace checks remain the gate commands. PR whitespace
uses head/base merge-base; first pushes use Git's empty tree. Checkout disables CRLF conversion
to preserve committed bytes on Windows. Windows contracts locate Git Bash across Git layouts;
the workflow exposes the pinned native Codex executable for Python's CLI preflight.

Credential-free local contract tests exercise source/tool/lock identity checks, valid and invalid
metadata, two real immutable package rebuilds, strict schema-v1 CI indexes and file digests,
rejected differing rebuilds, command exit/missing-result handling, aggregate rejection of
failed/cancelled/skipped/missing variants, and the separate manual behavioral preflight.
Observed local checks and each acceptance criterion are recorded in
[SLICE-DN-005](devquitect-next/slices/SLICE-DN-005.md), which owns delivery verification status.
The distributed slice verifier, its YAML inventory semantics, dependencies, skill contracts,
existing packaging version enforcement, and canonical report/promotion schemas are preserved.

`behavioral.yml` is an optional manual API-key workflow requiring explicit authorization,
configuration, and an exact reviewed `main` SHA. Missing authorization or configuration yields
`not-run`; there has been no dispatch, model run, credential configuration, or matrix-row update
in this delivery. Behavioral success cannot replace any deterministic gate.

Hosted [PR run 37264198908](https://github.com/3spGon/devquitect/actions/runs/37264198908)
tested integration `e5883c7bb2f112d7f81061553d7555f70a720c7a`, head
`4978cac9ef1b470b1c569be24cf811c08be7b384`, and base
`6230f4f3e831e5400db035c3de058e9cfe72946b` separately. Independent
[main push run 37264541061](https://github.com/3spGon/devquitect/actions/runs/37264541061)
verified exact final commit `1fb3c2f9a42cfb1861ab058fb257b1d1447e1930`; all six jobs succeeded
in both attempt-1 runs. Linux/macOS/Windows passed 89 smoke/contracts with actual Python 3.12;
canonical Linux used Python 3.12.14, uv 0.12.10, zlib 1.3 and locked dependencies. Source,
installed tool revision and workflow identity coincide for each distinct tested commit.

The canonical job built twice in independent roots and passed the equal ZIP/entry-manifest guard.
Downloaded schema-v1 CI indexes, ZIP/manifest/report sizes and SHA-256 digests were validated.
The final-main ZIP digest is `aa2deeb6dffb68ca28f31db03953bcf4ef46225e2b776fecdc51e7259a868ceb`.
Required names are `Devquitect / quality`, `Devquitect / platform-smoke`, and
`Devquitect / package`; the aggregate requires successful Linux/macOS/Windows variants. Earlier
failed Windows attempts were blocked by these gates and are retained as diagnostic history.
DN-006 CI-aware readiness, artifact consumption, and publication remain outside implemented scope.

## Technical landscape

The maintained skills remain declarative Markdown and YAML. Repository quality tooling uses Python 3.12 with a `src/` package layout, setuptools build metadata, a `uv.lock` dependency lock, PyYAML, jsonschema, pytest, and Ruff. Implemented components own source selection, read-only snapshots, structural validation, isolated Codex execution, bounded App Server JSON-RPC lifecycle control, normalized observations, deterministic assertions, behavioral cases, stable/candidate comparison, deterministic packaging, release-eligibility policy, canonical reporting, and the `devquitect` plugin definition. Publication remains manual and outside the tooling.

## Development and verification

The stable baseline and source-snapshot component are verified with:

```text
uv sync --all-groups
uv run pytest
uv run devquitect validate --source working-tree --format json
uv run ruff check src tests
git diff --exit-code -- skills
```

The proportional Change Profile candidate passed the skill-specific `quick_validate.py` check plus `tests/unit/test_cases.py` and `tests/integration/test_eval_command.py` with three focused tests passing. Five versioned Change Profile cases cover expedited routing, trust-sensitive elevation, stale context, legacy schema-v2 compatibility, and behavior-preserving refactor routing. Promotion requires a credential-free check bound to the exact candidate; working-tree checks do not substitute for it.

The fast suite verifies immutable reconstruction, source eligibility, post-freeze isolation, invalid source/path handling, structural records, report safety, fresh attempt boundaries, JSONL normalization, redaction, deterministic precedence, case contracts, paired snapshots, comparison policy, semantic-version policy, configurable behavioral defaults, package allowlists, normalized rebuilds, release evidence blocking, App Server lifecycle protocol handling, and integrated check exit/report behavior. The current SLICE-004 baseline also passes focused scenario, observation, assertion, routing, and fake-App-Server tests without credentials. Candidate commit `1e3f576b8b45cd4591c2b44cf883b6926cba4e55` passed the full trusted `check` with `gpt-5.4-mini`, reasoning effort `low`, eight critical runs, and clean-ref comparison `5e4a0da7-df75-48ad-b901-8fb769871533` against snapshot `sha256:062d5509956e73de366b9c351bb93441dcd39e2bf04cc8b6b870f797717960ef`. The `0.2.0` package rebuilt with digest `sha256:ce15c1cfb1966c69ebca32bfed9fbfcdbe41a1a054844360f70f90a026eeb5ba`; the promotion record remains an unapproved proposal.

## Preserved behavior

Future initiatives must preserve the distinct responsibility boundaries among software definition, authorized delivery, and targeted refactoring. They must not silently broaden implementation authority, conflate implemented work with verified work, or turn read-only requests into repository mutations. Gate 1 and Gate 2 remain explicit approvals even when an eligible expedited change combines their request; implementation still requires an approved plan and explicit slice authorization. Existing schema-v2 sessions without `change_profile` remain valid without migration. Ordinary `turns` evaluation and `codex exec` remain unchanged while lifecycle scenarios use the separate App Server adapter.

## Known limitations and context gaps

- Contributor checks and hosted PR/final-main CI have current credential-free evidence; changing
  source or runner/tool versions requires fresh candidate evidence.
- Behavioral checks require an explicit trusted run with ChatGPT or API authentication; ordinary fast checks remain credential-free.
- Compatibility across model or Codex runtime changes is not measured.
- Real lifecycle scenarios depend on the Codex App Server protocol and trusted
  authentication; adapter, hook, service, or same-thread lifecycle failures remain inconclusive.
- Model-backed evidence is candidate-specific and retained in local reports rather than this source baseline; it is review-only and cannot change promotion eligibility.
- CI artifacts expire after 30 days and are verification evidence, not public releases. DN-006
  CI-aware readiness, installation automation, and publication remain outside DN-005.
- The `0.4.0` candidate is not promoted until exact-commit evidence passes and a maintainer explicitly approves the resulting promotion proposal.

## Authoritative references

- [`software-idea-to-project`](../../skills/software-idea-to-project/SKILL.md)
- [Proportional Change Profile contract](../../skills/software-idea-to-project/references/change-profile.md)
- [`project-plan-execution`](../../skills/project-plan-execution/SKILL.md)
- [`targeted-refactoring`](../../skills/targeted-refactoring/SKILL.md)
- [Stable N manifest](../../baselines/stable-n.json)
- [Source snapshot implementation](../../src/devquitect_quality/sources.py)
- [Structural validator](../../src/devquitect_quality/validate.py)
- [Behavioral adapter](../../src/devquitect_quality/codex_adapter.py)
- [App Server lifecycle adapter](../../src/devquitect_quality/app_server_adapter.py)
- [Behavioral cases](../../evals/cases)
- [Comparison engine](../../src/devquitect_quality/comparison.py)
- [Plugin packager](../../src/devquitect_quality/packaging.py)
- [Promotion policy](../../src/devquitect_quality/promotion.py)
- [Contributor guidance](../../docs/contributing-skills.md)
- [Repository README](../../README.md)
- [Snapshot tests](../../tests/integration/test_stable_baseline.py)
