# Devquitect Skill Development System implementation plan

Status: Approved
Last updated: 2026-08-30
Plan revision: 1

## Confirmed

- Gate 1 and Gate 2 are approved for the concept, requirements, architecture, data model, contracts, and decisions referenced below.
- The repository currently contains three Markdown/YAML skills and no repository-owned runtime, test framework, plugin manifest, or CI configuration.
- Current repository evidence identifies Python 3.12.13, `uv` 0.11.19, Codex CLI 0.139.0, Git commit `264f4648ae1e699168347eb8e5945459bfbd0e27`, and preliminary tag `v0.1.0` at an older commit.
- No implementation slice may modify files under `skills/`; stable N must be frozen and verified before any later initiative creates N+1.
- Human interaction design is not applicable. Delivery exposes commands, schemas, reports, documentation, and plugin artifacts rather than a graphical interface.

## Assumptions

- Use Python 3.12, a `src/` package layout, setuptools as the build backend, and `uv.lock` as the exact Python dependency lock.
- Use PyYAML and jsonschema as runtime dependencies, with pytest and Ruff as development dependencies; exact transitive versions are committed in `uv.lock`.
- Treat commit `264f4648ae1e699168347eb8e5945459bfbd0e27` as stable N for the bootstrap record because it is the current immutable commit containing the skill versions used during definition.
- Store canonical generated reports under a caller-selected output path; temporary workspaces and raw runtime streams are not committed.

## Open decisions

No implementation-blocking decisions remain. Behavioral model matrices, repetition counts, retention limits, and semantic thresholds are deliberately calibrated from the baseline slice that first produces real behavioral evidence.

## Goal and observable outcome

A contributor can use one repository-owned Python command surface to validate skill structure, run isolated behavioral cases, compare stable N with a candidate, inspect versioned evidence, and build a reproducible `devquitect` plugin from a verified commit. Critical authorization and mutation regressions block release eligibility regardless of semantic scoring.

## Approved inputs

- [Concept](01-concept.md)
- [Requirements](02-requirements.md)
- [Architecture](04-architecture.md)
- [Data model](05-data-model.md)
- [Contracts](06-api-contracts.md)
- [Technical decisions](07-decisions.md)

## Global constraints and non-goals

- Preserve the responsibility and authorization boundaries of all existing skills.
- Do not edit `skills/` in this delivery plan.
- Do not install or publish a public marketplace plugin.
- Do not select or encode quality policy in a hosted CI provider.
- Do not add MCP servers, connectors, external-system mutation, a hosted evaluation service, or a graphical interface.
- Do not count an infrastructure failure or diagnostic-only run as passing release evidence.
- Do not use exact full-response snapshots as the primary behavioral contract.

## Proposed repository structure

All paths below are proposed except the existing `skills/` and `docs/software-design/` trees.

```text
.codex-plugin/plugin.json
pyproject.toml
uv.lock
baselines/stable-n.json
schemas/eval-case.schema.json
schemas/report.schema.json
schemas/promotion-record.schema.json
src/devquitect_quality/
evals/cases/
evals/fixtures/
evals/rubrics/
tests/unit/
tests/integration/
tests/contract/
docs/contributing-skills.md
```

## Delivery slices

### SLICE-001 — Freeze and verify stable N

**Outcome:** Establish the immutable trust anchor and Python test foundation before any candidate skill can be created.

**Dependencies:** Approved Gate 2 documents; Git object `264f4648ae1e699168347eb8e5945459bfbd0e27` must remain resolvable. No other slice may begin until this slice is verified.

**Files:** Create proposed `pyproject.toml`, `uv.lock`, `src/devquitect_quality/__init__.py`, `src/devquitect_quality/sources.py`, `src/devquitect_quality/models.py`, `baselines/stable-n.json`, `tests/unit/test_sources.py`, and `tests/integration/test_stable_baseline.py`. Read but do not modify verified `skills/*` at the stable commit.

**Interfaces and rules:**

- `SkillSource` resolves `git-ref` and `working-tree` selectors without following paths outside the repository.
- `freeze_source()` copies declared skill inputs to a temporary read-only snapshot, normalizes paths and modes, and computes a SHA-256 manifest digest.
- `baselines/stable-n.json` records schema version, exact commit, three skill names, per-file digests, aggregate digest, and creation tool identity.
- A working-tree snapshot is marked diagnostic-only; a clean Git revision can be a stable source.
- A missing Git object, path traversal, escaping symlink, changed baseline digest, or unexpected skill set fails explicitly.

**Acceptance and tests:**

- A post-freeze edit to a copied candidate fixture cannot alter the stable snapshot digest or contents.
- The baseline test materializes the recorded commit twice and obtains the same manifest.
- The baseline contains exactly `software-idea-to-project`, `project-plan-execution`, and `targeted-refactoring`.
- `git diff -- skills` is empty before and after the slice.

Verification commands:

```text
uv sync --all-groups
uv run pytest tests/unit/test_sources.py tests/integration/test_stable_baseline.py
uv run ruff check src tests
git diff --exit-code -- skills
```

**Documentation and evidence:** Store the baseline manifest and passing test output in the delivery checkpoint. Refresh System Context `Technical landscape`, `Development and verification`, and `Authoritative references` after verification to record the Python toolchain and immutable stable baseline as implemented facts.

### SLICE-002 — Structural validation and plugin definition

**Outcome:** Provide the credential-free `devquitect validate` command and reject malformed skills, cases, references, metadata, or package inputs before model execution.

**Dependencies:** SLICE-001.

**Files:** Create proposed `.codex-plugin/plugin.json`, `schemas/eval-case.schema.json`, `schemas/report.schema.json`, `schemas/promotion-record.schema.json`, `src/devquitect_quality/cli.py`, `src/devquitect_quality/validate.py`, `src/devquitect_quality/reporting.py`, `tests/unit/test_validate.py`, `tests/unit/test_reporting.py`, and structural fixtures under `tests/fixtures/`. Modify proposed `pyproject.toml` and `uv.lock`. Read verified `skills/*/SKILL.md`, `skills/*/agents/openai.yaml`, and referenced resources without changing them.

**Interfaces and rules:**

- Implement `devquitect validate --source <selector> [--format json|text] [--report <path>]`.
- Validate required frontmatter, directory/name equality, unique skill names, local reference existence, presentation metadata, declared plugin membership, schema compatibility, and package allowlists.
- Reports use the approved JSON envelope, atomic writes, normalized relative paths, and exit codes `0`, `1`, or `2`.
- Validation is offline and credential-free. Unsupported schemas and invalid toolchain/configuration use exit `2`; repository quality failures use exit `1`.

**Acceptance and tests:**

- Valid current skills and plugin metadata pass.
- Invalid frontmatter, name mismatch, duplicate name, missing reference, unexpected package file, unsupported schema, and unsafe path each fail with a specific machine-readable record.
- Text presentation and JSON serialization represent the same verdict.

Verification commands:

```text
uv run pytest tests/unit/test_validate.py tests/unit/test_reporting.py
uv run devquitect validate --source working-tree --format json
uv run ruff check src tests
```

**Documentation and evidence:** Add the structural authoring rules to proposed `docs/contributing-skills.md`. Refresh System Context `Current capabilities`, `Development and verification`, and `Known limitations` after verification.

### SLICE-003 — Isolated execution and deterministic observation

**Outcome:** Execute a fixture through a pinned Codex process in a fresh conversation/workspace and produce normalized observations suitable for deterministic assertions.

**Dependencies:** SLICE-002; Codex CLI 0.139.0 assumptions must pass contract preflight.

**Files:** Create proposed `src/devquitect_quality/fixtures.py`, `codex_adapter.py`, `observations.py`, `assertions.py`, `redaction.py`, `tests/unit/test_observations.py`, `tests/unit/test_assertions.py`, `tests/integration/test_fixture_isolation.py`, `tests/integration/test_fake_codex_run.py`, and `tests/contract/test_codex_cli_contract.py`. Add safe fixture repositories and fake JSONL streams under `tests/fixtures/`.

**Interfaces and rules:**

- Materialize one temporary Git workspace and isolated skill-discovery/configuration root per attempt.
- Invoke `codex exec --ephemeral --json` with explicit `--cd`, `--sandbox`, `--ignore-user-config`, and `--ignore-rules` settings validated by preflight.
- Normalize process status, runtime errors, messages, commands, tools, file changes, searches, Git diff, filesystem manifests, and persistent checkpoint fields.
- Implement side-effect-free assertions for Git cleanliness/diff, allowed and forbidden paths, command/tool policy, checkpoint transitions, required artifacts, and structured final output.
- Read-only is the default sandbox. `danger-full-access`, escaping writes, unparseable JSONL, missing terminal events, or leaked credential patterns prevent release eligibility.
- Adapter/authentication/service failure is exit `3` and inconclusive; it never passes or automatically retries.

**Acceptance and tests:**

- Parallel or sequential attempts cannot observe each other's conversation, files, installed skills, configuration, or evidence namespace.
- Fake JSONL contract fixtures cover successful completion, command/file events, runtime error, truncated stream, and unknown optional events.
- A read-only case that writes, an allowlist violation, and an invalid checkpoint transition fail deterministically.
- Tests run without model credentials; the real adapter has an explicit opt-in smoke command.

Verification commands:

```text
uv run pytest tests/unit/test_observations.py tests/unit/test_assertions.py tests/integration/test_fixture_isolation.py tests/integration/test_fake_codex_run.py tests/contract/test_codex_cli_contract.py
uv run ruff check src tests
```

Optional trusted smoke evidence:

```text
uv run devquitect eval --source 264f4648ae1e699168347eb8e5945459bfbd0e27 --case runtime-smoke
```

**Documentation and evidence:** Document credential scoping, sandbox limits, local raw-evidence retention, and exit `3` troubleshooting. Refresh System Context `Technical landscape` and `Development and verification` after verified real-adapter evidence exists; fake-adapter tests alone do not claim real runtime support.

### SLICE-004 — Behavioral evaluation and critical skill contracts

**Outcome:** Deliver `devquitect eval` with versioned cases covering routing, read-only behavior, authorization gates, verification claims, persistent state, and semantic criteria for all three skills.

**Dependencies:** SLICE-003.

**Files:** Create proposed `src/devquitect_quality/cases.py`, `grading.py`, eval cases under `evals/cases/`, isolated repositories under `evals/fixtures/`, rubrics under `evals/rubrics/`, `tests/unit/test_cases.py`, `tests/unit/test_grading.py`, and `tests/integration/test_eval_command.py`. Modify proposed `cli.py`, schemas, and report records.

**Interfaces and rules:**

- Implement `devquitect eval --source <selector> [--suite <name> | --case <id>] [--model <id>] [--reasoning-effort <level>]`.
- Cases declare fixed repetitions, activation type, fixture digest, sandbox, deterministic assertions, forbidden effects, and optional semantic rubric.
- The grader receives bounded normalized evidence without the candidate skill installed as an active grader instruction.
- Critical deterministic failures force `fail`; missing critical evidence forces `inconclusive`; semantic results cannot override either.
- Store model, effort, Codex version, grader identity, fixture digest, snapshot digest, timestamps, redactions, and evidence references.

**Acceptance and tests:**

- Positive and negative routing cases exist for each skill.
- Critical cases cover: read-only status/review mutation, Gate 1/Gate 2 bypass, execution without approved plan/slice authorization, verification claims without current execution, refactor edits during review/planning, hidden behavioral change, and incompatible handoff/state expectations.
- Exact prose is not required except for formal JSON/checkpoint contracts.
- A favorable fake semantic grade cannot erase an unauthorized write.
- Trusted baseline execution produces a calibration report; initial model matrix, repetitions, thresholds, and retention limit are then committed as reviewed configuration without changing approved hard invariants.

Verification commands:

```text
uv run pytest tests/unit/test_cases.py tests/unit/test_grading.py tests/integration/test_eval_command.py
uv run devquitect validate --source working-tree
uv run devquitect eval --source 264f4648ae1e699168347eb8e5945459bfbd0e27 --suite critical --report .devquitect-reports/stable-critical.json
uv run ruff check src tests
```

**Documentation and evidence:** Extend contributor documentation with case/rubric authoring, deterministic-versus-semantic guidance, fixed repetition policy, and report diagnosis. Refresh System Context `Current capabilities`, `Development and verification`, and `Known limitations` after trusted behavioral evidence verifies the runtime path.

### SLICE-005 — Stable/candidate comparison and self-hosting guardrail

**Outcome:** Deliver `devquitect compare` and prove that stable N can be used while candidate N+1 remains isolated and independently evaluated.

**Dependencies:** SLICE-004 and a verified stable baseline record from SLICE-001.

**Files:** Create proposed `src/devquitect_quality/comparison.py`, `tests/unit/test_comparison.py`, `tests/integration/test_compare_command.py`, and self-hosting/cross-skill cases and fixtures under `evals/`. Modify proposed CLI, report schema, and contributor documentation.

**Interfaces and rules:**

- Implement `devquitect compare --stable <selector> --candidate <selector> [--suite <name> | --case <id>]`.
- Freeze both selectors before either execution and use distinct conversations, workspaces, configuration roots, installed skills, and evidence namespaces.
- Classify compatible results as equivalent, improvement, regression, declared contract change, variable, or inconclusive.
- Require a reviewed declaration for accepted authorization, routing, persistent-state, or compatibility changes.
- A working-tree candidate remains diagnostic-only; comparison never converts it to release eligibility.

**Acceptance and tests:**

- Editing a candidate fixture after comparison starts cannot change the stable or candidate frozen digest.
- Neither execution can discover the other's skill snapshot.
- The self-hosting case has stable `software-idea-to-project` define a successor while preserving both approval gates and avoiding implementation authorization.
- A candidate that relaxes an authorization boundary is reported as a regression unless an explicit contract-change declaration and updated cases exist; declaration alone cannot override critical safety policy.

Verification commands:

```text
uv run pytest tests/unit/test_comparison.py tests/integration/test_compare_command.py
uv run devquitect compare --stable 264f4648ae1e699168347eb8e5945459bfbd0e27 --candidate working-tree --suite self-hosting --report .devquitect-reports/self-hosting.json
uv run ruff check src tests
```

**Documentation and evidence:** Document the exact procedure for installing/materializing stable N, creating N+1, interpreting diagnostic-only comparison, and recovering through manual/external authoring. Refresh System Context `Current capabilities` and `Preserved behavior` after verification.

### SLICE-006 — Reproducible packaging and release eligibility

**Outcome:** Build the `devquitect` plugin twice from an exact clean commit, verify identical content/digests, and produce a human-approvable promotion record without publishing.

**Dependencies:** SLICE-005; candidate source must be a clean Git commit and required behavioral evidence must identify the same contents.

**Files:** Create proposed `src/devquitect_quality/packaging.py`, `src/devquitect_quality/promotion.py`, `tests/unit/test_packaging.py`, `tests/unit/test_promotion.py`, and `tests/integration/test_release_check.py`. Modify proposed CLI, plugin manifest, schemas, and contributor documentation.

**Interfaces and rules:**

- Implement `devquitect package --source <clean-git-ref> --version <semver> --output <directory>` and `devquitect release-check --source <clean-git-ref> --version <semver> --evidence <path> --output <directory>`.
- Reject dirty/non-Git release sources, mismatched evidence commits/digests, unresolved critical cases, unsupported schema changes, missing migration/recovery coverage, and undeclared behavioral deltas.
- Archive allowlisted `.codex-plugin/plugin.json` and `skills/` inputs only; sort entries, normalize timestamps/modes/ownership, block traversal and escaping symlinks, and compute SHA-256.
- Build in two fresh roots and require identical entry manifests and artifact digests.
- Emit a proposed immutable `PromotionRecord`; only explicit human approval can complete promotion. No command publishes, tags, pushes, or installs.
- Rollback selects a prior recorded package; release history is not rewritten.

**Acceptance and tests:**

- The artifact contains exactly the manifest and three declared skills, including their declared resources/metadata, and excludes `.DS_Store`, archives, tests, reports, caches, and machine-local files.
- Same source/version/toolchain rebuilds identically; a changed input changes the digest.
- Patch/minor/major policy and persistent schema migration/recovery requirements are covered.
- An inconclusive run, critical failure, or candidate working-tree selector blocks release-check.

Verification commands:

```text
uv run pytest tests/unit/test_packaging.py tests/unit/test_promotion.py tests/integration/test_release_check.py
uv run devquitect package --source HEAD --version 0.2.0 --output dist
uv run devquitect release-check --source HEAD --version 0.2.0 --evidence .devquitect-reports --output dist
uv run ruff check src tests
```

**Documentation and evidence:** Document semantic version policy, compatibility declarations, package inspection, promotion approval, rollback, and the explicit absence of publication. Refresh System Context `Current lifecycle`, `Current capabilities`, `Development and verification`, and `Known limitations` after verification.

### SLICE-007 — Integrated contributor workflow and handoff

**Outcome:** Make `devquitect check` the documented local definition of done and verify the complete first-release workflow from contribution through proposed promotion evidence.

**Dependencies:** SLICE-001 through SLICE-006.

**Files:** Create proposed `README.md` and `tests/integration/test_check_command.py`, complete proposed `docs/contributing-skills.md`, and add end-to-end fixture coverage. Modify proposed `cli.py`, `pyproject.toml`, and `uv.lock` only as required by the integrated workflow. Do not create provider-specific CI configuration.

**Interfaces and rules:**

- Implement `devquitect check [--source <selector>] [--behavioral] [--report <path>]` by composing the existing engines, not duplicating policy.
- Default check is offline and credential-free: source/structural/schema validation plus unit, integration, and contract tests that use fake runtime evidence.
- `--behavioral` explicitly adds configured real behavioral suites and returns exit `3` for unresolved infrastructure.
- Contributor guidance covers create/change/review/test/compare/package/release-check, negative activation boundaries, allowed/prohibited effects, compatibility, evidence review, and recovery.

**Acceptance and tests:**

- A new-contributor walkthrough adds a fixture skill, catches an intentional metadata error, fixes it, runs checks, and packages only after clean-source requirements are met.
- All ten approved acceptance scenarios have automated coverage or an explicit trusted behavioral command with retained report identity.
- Every command returns the documented exit code and atomic report envelope for pass, fail, invalid input, and inconclusive infrastructure.
- Full fast suite passes without credentials; the trusted behavioral suite and release dry run reference exact snapshot/toolchain identities.

Verification commands:

```text
uv run devquitect check --source working-tree --report .devquitect-reports/check.json
uv run pytest
uv run ruff check src tests
uv run devquitect check --source HEAD --behavioral --report .devquitect-reports/full-check.json
```

**Documentation and evidence:** Record the complete command/evidence matrix in contributor documentation. Perform a final System Context refresh so orientation accurately names the implemented command surface, tests, plugin packaging, remaining lack of public publication/hosted CI, and the latest verified baseline reference.

## Requirement traceability

| Requirement | Delivery slice and verification |
|---|---|
| REQ-001 | SLICE-002 and SLICE-007; contributor walkthrough and integrated check |
| REQ-002 | SLICE-002; structural metadata tests and authoring guidance |
| REQ-003 | SLICE-002; invalid structural fixture matrix |
| REQ-004 | SLICE-004; positive/negative routing cases |
| REQ-005 | SLICE-003; fixture/conversation isolation integration tests |
| REQ-006 | SLICE-003 and SLICE-004; normalized observations and assertion coverage |
| REQ-007 | SLICE-004; semantic rubric and non-golden response tests |
| REQ-008 | SLICE-003 and SLICE-004; deterministic failure precedence test |
| REQ-009 | SLICE-003 and SLICE-004; bounded evidence and redaction tests |
| REQ-010 | SLICE-004; read-only mutation cases |
| REQ-011 | SLICE-004; unapproved plan/slice execution cases |
| REQ-012 | SLICE-004; verification-without-execution cases |
| REQ-013 | SLICE-004; refactor review/planning and hidden-change cases |
| REQ-014 | SLICE-004 and SLICE-005; gate and self-hosting cases |
| REQ-015 | SLICE-004 and SLICE-005; cross-skill handoff/state cases |
| REQ-016 | SLICE-001 and SLICE-005; stable/candidate identities |
| REQ-017 | SLICE-001 and SLICE-005; frozen-snapshot mutation tests |
| REQ-018 | SLICE-003 through SLICE-005; report provenance assertions |
| REQ-019 | SLICE-005; paired independent execution |
| REQ-020 | SLICE-004 through SLICE-006; grader/policy/human promotion separation |
| REQ-021 | SLICE-005; self-hosting behavioral case |
| REQ-022 | SLICE-005 and SLICE-007; manual/external recovery documentation and case |
| REQ-023 | SLICE-006; clean source and allowlist packaging tests |
| REQ-024 | SLICE-006; two-root rebuild digest test |
| REQ-025 | SLICE-004 and SLICE-006; critical failure release blocking |
| REQ-026 | SLICE-004 and SLICE-006; schema migration/recovery cases |
| REQ-027 | SLICE-006; patch/minor/major policy tests |
| REQ-028 | SLICE-005 through SLICE-007; comparison and promotion evidence |

## Approved acceptance-scenario coverage

| Scenario | Primary slice |
|---:|---|
| 1 | SLICE-007 contributor walkthrough |
| 2 | SLICE-002 invalid structural fixtures |
| 3 | SLICE-004 routing evidence |
| 4 | SLICE-003/004 deterministic write prohibition |
| 5 | SLICE-005 stable/candidate isolation |
| 6 | SLICE-001/005 snapshot immutability |
| 7 | SLICE-001/006 commit and artifact provenance |
| 8 | SLICE-005/006 declared contract-change policy |
| 9 | SLICE-004/006 migration and recovery coverage |
| 10 | SLICE-006 deterministic package allowlist |

## Risk treatment and residual monitoring

| Risk | Treatment | Residual signal |
|---|---|---|
| Candidate contaminates stable author | SLICE-001 content-addressed baseline and SLICE-005 isolated discovery roots | Digest mismatch or unexpected discovered skill makes run ineligible |
| Model variability masks regression | Fixed repetitions, paired comparisons, hard deterministic invariants | Variable/inconclusive classifications and calibrated suite report |
| Codex CLI event contract changes | Pinned version identity and SLICE-003 contract tests | Preflight or event parser failure uses exit `3` |
| Credentials leak to fixtures/evidence | Subprocess scoping, redaction, trusted execution policy | Secret-pattern test and redaction manifest |
| Reproducible package differs across environments | Normalized archive plus clean two-root rebuild | Entry or artifact digest mismatch blocks release |
| Baseline definition becomes stale | Immutable baseline records and explicit promotion records | New successor requires a new reviewed baseline record |
| Hosted CI remains absent | Provider-neutral commands and reports | Local/trusted execution remains required; public automation is deferred |

## Delivery ordering and authorization boundary

Slices execute in numeric order. SLICE-001 is a hard prerequisite: if the stable baseline cannot be reconstructed exactly, delivery stops before implementing later infrastructure and before any N+1 skill edit. Subsequent slices may be authorized individually or as an explicit list.

This plan is definition only. Approval of this document completes the software-definition workflow but does not authorize implementation, dependency installation, commits, tags, publication, or execution of any slice. Implementation requires a separate explicit request naming the authorized `SLICE-*` set and then transfers to `project-plan-execution`.
