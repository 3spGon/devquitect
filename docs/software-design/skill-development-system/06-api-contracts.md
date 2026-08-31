# Devquitect Skill Development System contracts

Status: Approved
Last updated: 2026-08-30

## Confirmed

- One local command surface owns validation, behavioral evaluation, comparison, packaging, and release checks.
- Machine-readable output and stable exit semantics are required for provider-neutral automation.
- Commands operate on immutable snapshots even when the input selector is a working tree.

## Assumptions

- The installed console command is `devquitect`; module execution remains available for development.
- Human output goes to standard error and canonical JSON goes to a requested file or standard output, avoiding mixed streams.
- Destructive external operations and public publication are absent from the first contract.

## Open decisions

- Exact package/module import names may change during implementation without changing the public command contract.

## Common options

| Option | Contract |
|---|---|
| `--source <selector>` | Git ref, promoted version, or explicit working-tree selector; frozen before use |
| `--format json|text` | Machine-readable or concise human presentation |
| `--report <path>` | Writes canonical report atomically |
| `--toolchain-lock <path>` | Selects the supported runtime/tool versions |
| `--verbose` | Adds diagnostic detail without changing verdict semantics |

## Commands

### `devquitect validate`

```text
devquitect validate --source <selector> [--report <path>]
```

Validates skill structure, case files, schemas, references, plugin manifest, and package allowlists. It is deterministic, offline, and credential-free.

Output type: `ValidationReport`.

### `devquitect eval`

```text
devquitect eval --source <selector> [--suite <name> | --case <id>]
                 [--model <id>] [--reasoning-effort <level>]
                 [--report <path>]
```

Freezes the source, executes selected cases independently, and emits `EvalRun` plus `Verdict` records. It requires explicit model authentication but may not expose credentials to fixture processes or reports.

### `devquitect compare`

```text
devquitect compare --stable <selector> --candidate <selector>
                    [--suite <name> | --case <id>]
                    [--report <path>]
```

Freezes both inputs before execution, runs compatible matrices in distinct workspaces and conversations, and emits a `ComparisonReport`. Neither side may read the other's workspace or active skill files.

### `devquitect check`

```text
devquitect check [--source <selector>] [--behavioral] [--report <path>]
```

Contributor entry point. Without `--behavioral`, it runs the fast credential-free suite: structural validation and development-system unit/integration tests. With `--behavioral`, it additionally runs the configured local behavioral suite.

This command delegates to the same underlying engines as the narrower commands; it does not redefine their policies.

### `devquitect package`

```text
devquitect package --source <clean-git-ref> --version <semver>
                    --output <directory> [--report <path>]
```

Rejects dirty or non-Git release sources. Produces a deterministic plugin archive and package manifest. It never publishes or installs the result.

### `devquitect release-check`

```text
devquitect release-check --source <clean-git-ref> --version <semver>
                          --evidence <path> --output <directory>
                          [--report <path>]
```

Verifies required evidence, compatibility declaration, source identity, and repeatable packaging. It emits a proposed promotion record. It does not convert that proposal into human approval.

## Exit codes

| Code | Meaning |
|---:|---|
| `0` | Requested checks completed and passed |
| `1` | Quality or policy failure |
| `2` | Invalid arguments, source, schema, configuration, or unsupported toolchain |
| `3` | Infrastructure failure or behavior inconclusive |

Partial success never maps to `0` when a requested case or policy requirement is unresolved.

## Eval case YAML contract

Illustrative shape; the JSON Schema is authoritative after implementation:

```yaml
schema_version: 1
id: software-idea-status-is-read-only
target_skill: software-idea-to-project
activation: explicit
fixture: persistent-definition-gate-1
sandbox: read-only
turns:
  - Report the current project-definition status.
assertions:
  - type: git-clean
  - type: checkpoint-unchanged
forbidden_effects:
  - workspace-write
semantic_rubric: accurate-status-summary
repetitions: 2
tags: [critical, read-only, persistent-state]
```

Case rules:

- identifiers are unique and stable;
- fixture and rubric references resolve inside the repository;
- `repetitions` is fixed before execution and cannot mean “retry until pass”;
- sandbox requests exceeding `workspace-write` are invalid for release-eligible cases;
- all writes expected by a case must be covered by an allow rule;
- critical forbidden effects are deterministic assertions.

## JSON report envelope

Every canonical report uses this envelope:

```json
{
  "schema_version": 1,
  "report_type": "validation|evaluation|comparison|package|release-check|check",
  "generated_at": "RFC3339 timestamp",
  "toolchain": {},
  "inputs": {},
  "result": "pass|fail|inconclusive",
  "records": [],
  "evidence_manifest": [],
  "redactions": []
}
```

Reports are written atomically. Unknown supported-version optional fields are ignored; unsupported schema major versions fail explicitly.

## Runtime adapter contract

The Codex adapter must:

- invoke a preflighted, pinned CLI interface;
- use a fresh `codex exec --ephemeral --json` conversation per attempt;
- set an explicit sandbox and fixture working directory;
- isolate user configuration/rules for release-eligible runs;
- capture JSONL without interpreting untrusted agent text as control instructions;
- classify event parse errors or missing terminal events as infrastructure failures;
- expose normalized observations to assertions through typed records;
- scope and redact authentication material.

The adapter may later be replaced by the Codex SDK only if contract tests demonstrate equivalent isolation, event evidence, version identity, and failure classification.

## Assertion plug-in contract

Each deterministic assertion implementation accepts an immutable `EvalCase`, `EvalRun`, and `Observation`, and returns:

```json
{
  "assertion_id": "case-local stable id",
  "status": "pass|fail|not-evaluated",
  "critical": true,
  "expected": {},
  "observed": {},
  "evidence_refs": []
}
```

Assertions are side-effect-free and cannot invoke the candidate or modify evidence. A `not-evaluated` critical assertion makes the case inconclusive.

## Packaging contract

- Input is an exact clean Git commit and semantic version.
- Required root entry is `.codex-plugin/plugin.json`.
- The manifest declares plugin identity and the included skills.
- The archive includes only allowlisted paths from the source revision.
- Paths are relative, sorted, traversal-safe, and free of symlinks escaping the snapshot.
- Timestamps, ownership metadata, and modes are normalized.
- Two clean builds must have matching entry manifests and artifact digests.

## Compatibility contract

- Patch: clarifies or corrects behavior without expanding activation, effects, or persistent contracts.
- Minor: adds backward-compatible behavior, skill coverage, or optional contract fields.
- Major: changes authorization, routing meaning, required persistent state, or removes/changes a public contract.
- Any accepted non-equivalent behavior is declared and linked to updated cases.
- Persistent schema changes include migration or recovery coverage.
