# Devquitect Skill Development System data model

Status: Approved
Last updated: 2026-08-30

## Confirmed

- Configuration and evidence formats require explicit schema versions.
- Source provenance, observations, deterministic results, semantic results, and promotion decisions are distinct records.
- An infrastructure error is inconclusive and cannot be represented as a successful evaluation.

## Assumptions

- Human-authored cases use YAML for readability and validate against repository-owned JSON Schemas.
- Canonical reports and promotion records use JSON for deterministic machine consumption.
- Filesystem evidence stores normalized relative paths and digests; raw workspace copies are not canonical evidence.

## Open decisions

- Retention limits for local raw event streams will be calibrated during implementation.
- Exact semantic scoring dimensions will be established with the first rubrics.

## Aggregate relationships

```text
SkillSnapshot 1 --- * EvalRun * --- 1 EvalCase
                         |
                         +--- * Observation
                         +--- 1 Verdict

Comparison 1 --- 1 stable Verdict
           +--- 1 candidate Verdict

PromotionRecord 1 --- * release-eligible Verdict
                +--- * accepted delta
                +--- 1 PackageArtifact
```

## SkillSource

Describes an input before it is frozen.

| Field | Meaning |
|---|---|
| `kind` | `git-ref`, `working-tree`, or `promoted-release` |
| `selector` | User-provided ref, path, or version |
| `repository_root` | Resolved repository identity, not serialized into portable reports as a machine-local absolute path |
| `resolved_commit` | Commit SHA when available |
| `dirty` | Whether the originating working tree differed from its commit |

## SkillSnapshot

Immutable execution input derived from a `SkillSource`.

| Field | Meaning |
|---|---|
| `snapshot_id` | Content-addressed identifier |
| `source_kind` | Original source type |
| `resolved_commit` | Originating commit, if any |
| `working_tree_fingerprint` | Digest of candidate changes when source was dirty |
| `content_digest` | Digest of the normalized snapshot manifest |
| `skills` | Names, relative paths, and per-skill digests |
| `created_at` | Snapshot time |
| `release_eligible_source` | True only for a clean identified revision or promoted release |

Snapshots are immutable. A new working-tree edit creates a new identity rather than mutating an existing snapshot.

## EvalCase

Versioned behavioral contract.

| Field | Meaning |
|---|---|
| `schema_version` | Case schema compatibility version |
| `id` | Stable repository-unique case identifier |
| `target_skill` | Skill primarily under test |
| `activation` | `explicit`, `implicit-positive`, `implicit-negative`, or `cross-skill` |
| `fixture` | Fixture identity and expected digest |
| `turns` | Ordered user inputs for a fresh conversation |
| `sandbox` | Minimum required capability: `read-only` or `workspace-write` |
| `assertions` | Deterministic observable expectations |
| `forbidden_effects` | Actions or state transitions that must not occur |
| `semantic_rubric` | Optional rubric identifier |
| `repetitions` | Fixed measurement count, never an until-pass retry |
| `tags` | Suite, risk, skill, and compatibility selectors |

Assertion types include final structured contract, command occurrence or prohibition, path presence/absence/content digest, allowed change set, Git status/diff, checkpoint transition, artifact state, and runtime exit class.

## EvalRun

One attempt for one case against one immutable snapshot.

| Field | Meaning |
|---|---|
| `run_id` | Unique attempt identifier |
| `case_id` / `case_digest` | Exact case contract executed |
| `snapshot_id` | Exact evaluated skill contents |
| `role` | `stable`, `candidate`, or `standalone` |
| `fixture_digest` | Exact initial workspace state |
| `codex_version` | Observed CLI/runtime version |
| `model` / `reasoning_effort` | Runtime configuration |
| `grader_identity` | Independent grader configuration when used |
| `started_at` / `finished_at` | Execution interval |
| `eligibility_context` | Whether configuration isolation and credential policy permit release use |

## Observation

Normalized evidence produced by an `EvalRun`.

| Field | Meaning |
|---|---|
| `runtime_status` | Exit status, signal, and classified runtime errors |
| `events` | Bounded normalized command, tool, file, search, plan, and message events |
| `final_response` | Final agent response or structured output |
| `filesystem_before` / `filesystem_after` | Relative-path manifests and digests |
| `git_before` / `git_after` / `git_diff` | Repository effects when applicable |
| `persistent_state` | Relevant before/after checkpoint fields and artifact states |
| `redactions` | Evidence fields removed or masked by policy |

## Verdict

| Field | Meaning |
|---|---|
| `classification` | `pass`, `fail`, or `inconclusive` |
| `deterministic_checks` | Individual results with expected and observed values |
| `critical_failures` | Non-overridable failed invariants |
| `semantic_grades` | Optional rubric dimensions, rationale, and grader identity |
| `eligibility` | `release-eligible`, `diagnostic-only`, or `not-eligible` |
| `evidence_refs` | Content-addressed links to bounded evidence |

Rules:

- any critical deterministic failure makes the verdict `fail`;
- infrastructure failure makes it `inconclusive`, never `pass`;
- semantic success cannot change a deterministic failure;
- a diagnostic-only run cannot satisfy promotion policy.

## Comparison

Pairs stable and candidate results for the same case and compatible runtime matrix.

| Field | Meaning |
|---|---|
| `comparison_id` | Unique comparison identifier |
| `stable_run_ids` | Stable repetitions |
| `candidate_run_ids` | Candidate repetitions |
| `case_digest` | Shared case contract |
| `delta` | Normalized behavioral and effect difference |
| `classification` | `equivalent`, `improvement`, `regression`, `contract-change`, `variable`, or `inconclusive` |
| `declaration_ref` | Required reviewed declaration for accepted contract changes |

## PackageArtifact

| Field | Meaning |
|---|---|
| `plugin_name` | `devquitect` |
| `version` | Semantic version |
| `source_commit` | Clean commit used for the build |
| `toolchain` | Compatible packager identity |
| `entries` | Sorted path, size, mode, and digest manifest |
| `artifact_digest` | SHA-256 of the normalized package |
| `rebuild_digest` | Independent second-build digest |

## PromotionRecord

Immutable release decision evidence.

| Field | Meaning |
|---|---|
| `schema_version` | Promotion schema version |
| `version` | Candidate release version |
| `source_commit` / `snapshot_id` | Exact promoted input |
| `package_digest` | Verified artifact identity |
| `run_ids` / `comparison_ids` | Evidence satisfying policy |
| `accepted_deltas` | Explicitly reviewed non-equivalent behavior |
| `compatibility` | `patch`, `minor`, or `major` impact and migration references |
| `residual_risks` | Known limitations accepted by the maintainer |
| `approved_by` / `approved_at` | Human decision provenance |

## Candidate lifecycle

```text
Draft
  -> Structurally Valid
  -> Behaviorally Evaluated
  -> Release Eligible
  -> Promoted
```

- Editing a snapshot creates a new Draft candidate.
- A failed structural or critical behavioral check moves the current evidence to Failed but does not delete it.
- Inconclusive infrastructure results leave the candidate unevaluated for the affected policy requirement.
- Release Eligible is computed from policy and evidence; Promoted additionally requires human approval and an immutable promotion record.

## Compatibility and migration

- Additive optional fields preserve the current schema version.
- Removing fields, changing meanings, or tightening required fields increments the schema version.
- Readers reject unsupported major schema versions with exit code `2` rather than guessing.
- Case and report migrations are explicit, deterministic transformations with fixture coverage.
- Skill persistent-state schema changes require recovery or migration scenarios before release eligibility.
