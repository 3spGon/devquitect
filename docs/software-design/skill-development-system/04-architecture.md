# Devquitect Skill Development System architecture

Status: Approved
Last updated: 2026-08-30

## Confirmed

- The first implementation is repository-local tooling around the three existing skills; it does not rewrite their behavior.
- Behavioral evaluation must observe effects in isolated conversations and workspaces.
- Stable and candidate skill sources must be immutable for the duration of a run and independently identifiable.
- Release eligibility remains a deterministic policy decision plus human approval; a candidate cannot approve itself.

## Assumptions

- Python 3.12 is the orchestration language because it is already available in the development environment and supports portable filesystem, subprocess, schema, and test tooling.
- The behavioral adapter invokes pinned Codex CLI behavior through `codex exec --ephemeral --json`; the Python SDK remains a future adapter option if it exposes equivalent evidence and isolation guarantees.
- Initial behavioral fixtures do not require external network access beyond the model invocation performed by Codex.
- CI integration is an adapter over the same local commands rather than a second quality implementation.

## Open decisions

- Exact model and reasoning-effort matrices will be selected after baseline runs expose cost and variance.
- Initial repetition counts and semantic thresholds will be calibrated from representative cases rather than chosen without evidence.
- A hosted CI provider is intentionally not selected in this design.

## Architectural drivers

1. Protect authorization, mutation, and persistence boundaries with deterministic assertions.
2. Make model-dependent behavior diagnosable without coupling tests to exact prose.
3. Prevent the live working tree or candidate from silently becoming the trusted stable evaluator.
4. Produce equivalent results locally and in any later CI environment.
5. Bind every evaluated and packaged result to exact source, fixture, runtime, and configuration identities.

## Context and trust boundaries

```text
maintainer / contributor
          |
          v
  local quality CLI -----------------------+
          |                                |
          v                                v
 structural validation              snapshot manager
                                           |
                           +---------------+---------------+
                           |                               |
                           v                               v
                 immutable stable N             immutable candidate N+1
                           |                               |
                           +---------------+---------------+
                                           |
                                           v
                              isolated case workspaces
                                           |
                                           v
                                pinned Codex adapter
                                           |
                                           v
                       observations -> assertions -> verdicts
                                           |
                                           v
                         comparison and promotion evidence
                                           |
                               human approval required
                                           |
                                           v
                              reproducible plugin package
```

The stable source, candidate source, case workspace, grader context, and release artifact are separate trust domains. No domain may obtain trust merely by writing a favorable result about itself.

## Components

### 1. Source registry and snapshot manager

Resolves a source selector to an immutable snapshot and manifest. A stable source must be a clean Git revision or promoted release. A candidate may originate from the working tree, but it is copied once into an immutable temporary snapshot before execution. Every file is hashed; subsequent working-tree edits cannot alter an in-progress run.

Responsibilities:

- resolve Git revisions and working-tree candidates;
- reject ambiguous or missing sources;
- copy only declared evaluation inputs;
- compute snapshot and per-file SHA-256 digests;
- identify dirty state without treating it as a releasable revision;
- materialize the selected skills into an isolated discovery root.

### 2. Structural validator

Performs credential-free validation before any model call. It checks skill directory conventions, `SKILL.md` frontmatter, name uniqueness and consistency, referenced local resources, presentation metadata, schema versions, plugin manifest contents, and package allowlists.

Structural failures are quality failures and prevent behavioral execution when later results would be misleading.

### 3. Fixture materializer

Creates a fresh temporary root for every case and attempt. It installs only the selected skill snapshot, copies the declared fixture, initializes Git when requested, and records a pre-run filesystem and repository state.

Release-eligible runs isolate or suppress user-global configuration, rules, and skills. If contamination cannot be excluded, the run is marked non-release-eligible rather than silently trusted.

### 4. Codex execution adapter

Runs each scenario in a fresh ephemeral conversation and emits the runtime's JSONL event stream. It uses an explicit sandbox profile per case: read-only by default and workspace-write only when the scenario requires mutation. Full-access execution is outside release-eligible scope.

The adapter preflights the exact CLI version and supported flags. Runtime or authentication failures are classified as infrastructure errors, not passing behavior. Credentials are scoped to the subprocess and are never copied into fixtures or reports.

### 5. Observation collector

Normalizes evidence without depending on exact response prose:

- process exit and runtime errors;
- agent final response and bounded transcript excerpts;
- command, tool, search, and file-change events exposed by the runtime;
- pre/post filesystem inventory and content digests;
- Git status and diff;
- persistent checkpoint state and declared artifacts;
- fixture, source, model, effort, and toolchain identity.

Raw evidence may be retained locally under a bounded policy; canonical reports redact secrets and avoid unnecessary transcript volume.

### 6. Deterministic assertion engine

Evaluates schema, routing markers, command policy, file allow/deny rules, Git state, approval gates, persistent-state transitions, artifact presence, and forbidden effects. Critical deterministic failures cannot be overridden by semantic grading.

### 7. Independent semantic grader

Scores only behavior that cannot be made reliably deterministic, such as whether a response meaningfully addresses the requested decision. It receives a bounded evidence projection and rubric, not the candidate skill as an active instruction source. Grader identity and configuration are recorded.

Semantic grading supplements deterministic assertions; it never grants authorization, erases an observed mutation, or promotes a release.

### 8. Comparison and promotion engine

Runs the same case definitions independently against stable N and candidate N+1, then classifies differences as regression, declared improvement, accepted contract change, variability, or inconclusive infrastructure result.

Promotion eligibility requires:

- an identified clean candidate commit;
- all structural and critical deterministic checks passing;
- required behavioral suites meeting their calibrated policy;
- declared compatibility and migration handling where applicable;
- a complete promotion record;
- explicit human approval.

### 9. Plugin packager

Builds `devquitect` from an identified clean Git revision. The package contains `.codex-plugin/plugin.json`, the declared `skills/` tree, and no test evidence, machine-local files, caches, or undeclared inputs. Entries are sorted and metadata normalized so rebuilding with a compatible toolchain yields equivalent contents and digest.

### 10. Reporting and CI adapter

Writes canonical machine-readable JSON and a concise Markdown summary. CI calls the same local commands and publishes the same artifacts; provider-specific workflow files contain orchestration only.

## Repository shape

The implementation-ready plan may refine names, but responsibilities should map approximately to:

```text
.codex-plugin/plugin.json
pyproject.toml
src/devquitect_quality/
  cli.py
  sources.py
  validate.py
  fixtures.py
  codex_adapter.py
  observations.py
  assertions.py
  grading.py
  comparison.py
  packaging.py
schemas/
  eval-case.schema.json
  report.schema.json
  promotion-record.schema.json
evals/
  cases/
  fixtures/
  rubrics/
tests/
  unit/
  integration/
docs/
  contributing-skills.md
```

## Execution flows

### Local structural check

1. Resolve and snapshot the requested source.
2. Validate repository, skills, schemas, and plugin manifest without credentials.
3. Return a stable exit code and JSON report.

### Behavioral case

1. Validate the case and selected snapshot.
2. Create a new temporary fixture root and install only that snapshot.
3. Record pre-state and start a fresh ephemeral Codex execution.
4. Collect runtime events and post-state.
5. Evaluate deterministic assertions.
6. Run semantic grading only when the case requires it and deterministic prerequisites permit it.
7. Emit a verdict; destroy the execution workspace while retaining bounded declared evidence.

### Stable-candidate comparison

1. Freeze stable N and candidate N+1 independently.
2. Execute each selected case in separate workspaces and conversations.
3. Compare normalized verdicts and observations, never mutable directories.
4. Require an explicit declaration for accepted behavioral contract changes.

### Release

1. Require a clean candidate commit and declared semantic version.
2. Execute release checks against that exact commit snapshot.
3. Build the plugin twice in clean temporary roots and compare manifests and digests.
4. Generate a promotion record from observed evidence.
5. Require human approval before marking the version promoted.

## Isolation and security

- Every attempt receives a fresh workspace, conversation, configuration boundary, and evidence namespace.
- Stable and candidate files are read-only after snapshot creation.
- Cases declare the minimum sandbox capability they need.
- Release-eligible execution does not use full-access mode.
- User rules, global skills, and local machine configuration are ignored or isolated; otherwise eligibility is denied.
- Untrusted contribution code must not run in a CI context holding long-lived model credentials.
- API credentials exist only for the Codex subprocess and are redacted from events and reports.
- Fixtures are offline by default and may not mutate systems outside their temporary root.

## Failure and recovery policy

- Quality failure: the system ran and an assertion or policy failed. Exit code `1`.
- Invalid input or toolchain: source, case, schema, version, or required runtime is invalid. Exit code `2`.
- Infrastructure/inconclusive: model service, authentication, or runner failed before behavior could be established. Exit code `3`; it never counts as a pass.
- Interrupted runs retain a partial run record but cannot produce promotion evidence.
- A failed stable self-hosting path may be replaced by manual or external authoring, but the resulting candidate enters the same independent validation pipeline.
- Rollback installs the prior immutable promoted package; promotion records and source tags are never rewritten.

## Test strategy for the development system itself

- Unit tests cover parsing, snapshots, digests, assertions, redaction, comparison, exit codes, and deterministic packaging.
- Integration tests use fake JSONL runtime streams and temporary Git repositories to exercise the full pipeline without model credentials.
- Contract tests pin the supported Codex CLI event and flag assumptions.
- Behavioral evals exercise the actual skills and runtime, separated from ordinary fast tests.
- Packaging tests build twice from the same fixture revision and compare contents and hashes.

## Deployment and operations

There is no long-running service. Maintainers install the Python development environment and invoke repository commands locally. A later CI job may run fast checks on every trusted change, behavioral suites under an explicit credential policy, and release checks only for a clean commit selected for promotion.

## Requirements traceability

| Requirements | Primary design coverage |
|---|---|
| REQ-001–004 | Contributor documentation, structural validator, routing cases, versioned case schema |
| REQ-005–009 | Fixture materializer, Codex adapter, observation collector, assertion/grading split, bounded evidence |
| REQ-010–015 | Deterministic critical assertions and cross-skill behavioral suites |
| REQ-016–022 | Source registry, immutable snapshots, stable-candidate comparison, independent grading, self-hosting and recovery flows |
| REQ-023–028 | Clean-revision packaging, normalized rebuilds, compatibility contracts, promotion records, human approval |

## Authoritative technical evidence

- Codex skills are the authoring unit, while plugins package and distribute one or more skills: [Build skills](https://developers.openai.com/codex/skills) and [Plugins](https://developers.openai.com/codex/plugins).
- Non-interactive Codex supports ephemeral execution, JSONL events, explicit sandboxes, ignored user configuration/rules, and structured output: [Non-interactive mode](https://developers.openai.com/codex/noninteractive).
- A Python SDK is available as a future adapter, but this design chooses the documented CLI event stream for its initial evidence boundary: [Codex SDK](https://developers.openai.com/codex/sdk).
