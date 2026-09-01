# Contributing skills

Devquitect skills are packaged together but retain separate, focused responsibilities. Structural validation is offline and must pass before behavioral evaluation or packaging.

## Required structure

Create a skill at `skills/<skill-name>/` where `<skill-name>` is unique, kebab-case, and exactly matches the `name` in `SKILL.md` frontmatter. The frontmatter also requires a non-empty `description` that states both when to use the skill and when not to use it.

Every skill includes `agents/openai.yaml` with non-empty `interface.display_name`, `interface.short_description`, and `interface.default_prompt` values. Local resources must be linked from `SKILL.md` with relative Markdown links, must remain inside the skill directory, and must exist as regular files. Unreferenced files, escaping paths, and symlinks are not eligible plugin inputs.

The root `.codex-plugin/plugin.json` identifies the `devquitect` plugin and declares `"skills": "./skills/"`. Its name is stable kebab-case, its version follows semantic versioning, and its component paths are relative to the plugin root.

## Validate a contribution

From the repository root, run:

```text
uv run devquitect validate --source working-tree --format text
uv run devquitect validate --source working-tree --format json --report .devquitect-reports/validation.json
```

Exit `0` means every requested structural check passed. Exit `1` identifies repository quality failures such as malformed skill metadata, missing references, duplicate names, or unexpected package inputs. Exit `2` means the selected source, schema, or validator configuration is invalid or unsupported. Validation does not require credentials or network access.

## Contributor walkthrough

1. Copy an existing minimal fixture into `skills/<new-name>/`, then change the directory name,
   `SKILL.md` frontmatter name/description, presentation metadata, and every local reference.
2. Add positive activation cases and negative cases that prove adjacent skills do not activate.
   Declare the minimum sandbox and make allowed and prohibited effects observable.
3. Intentionally run `uv run devquitect check --source working-tree` before fixing a metadata
   mismatch. Confirm exit `1` identifies the structural record, fix it, and rerun until exit `0`.
4. Review the atomic check report and the Git diff. Commit the complete candidate only after review;
   working-tree evidence remains diagnostic.
5. Run trusted comparison only when behavioral evidence is required. Package only the exact clean
   commit whose plugin manifest already contains the requested version.

## Command and evidence matrix

| Stage | Command | Credentials | Retained evidence |
|---|---|---|---|
| Author/validate | `devquitect validate --source working-tree` | No | Validation envelope and records |
| Local definition of done | `devquitect check --source working-tree` | No | Validation identity plus fast-suite exit |
| Behavioral evaluation | `devquitect eval --source <ref> --suite critical` | Trusted only | Run, case, snapshot, toolchain, and redaction identities |
| Stable/candidate review | `devquitect compare --stable <ref> --candidate <ref>` | Trusted only | Paired run and comparison identities |
| Full trusted check | `devquitect check --source <ref> --behavioral` | Trusted only | Composed validation, test, evaluation, and comparison evidence |
| Package | `devquitect package --source <ref> --version <version> --output dist` | No | Entry manifest, source commit, snapshot, and artifact digest |
| Release eligibility | `devquitect release-check ...` | No model call | Rebuild identity and unapproved promotion proposal |

The fast check invokes unit, integration, and Codex CLI contract coverage backed by fake runtime
streams; its own integration wrapper is exercised by the outer full suite to avoid recursive test
execution. Invalid input still writes a `check` report and exits `2`. Real adapter/service failures
make behavioral checks inconclusive and exit `3`; they are never converted into a pass.

JSON output and atomic report files use the versioned canonical envelope in `schemas/report.schema.json`. Paths in records are normalized and repository-relative. Text output represents the same verdict and issue records without changing exit semantics.

## Runtime isolation and evidence safety

Every behavioral attempt uses a fresh temporary Git workspace, Codex conversation, `CODEX_HOME`, installed-skill root, and evidence namespace. The supported adapter is pinned to Codex CLI `0.139.0` and invokes `codex exec --ephemeral --json` with an explicit working directory, `read-only` or `workspace-write` sandbox, `--ignore-user-config`, and `--ignore-rules`. `danger-full-access` is never release-eligible.

The isolated `CODEX_HOME` contains no user configuration. For trusted local execution, the runner may stage the existing file-backed ChatGPT login cache with permissions `0600` only for the lifetime of the subprocess, then removes it immediately. The cache never enters the fixture workspace, evidence namespace, repository, or report. Environment-provided authentication follows the same subprocess-only boundary. Known credential values and common secret patterns are masked before normalized evidence is retained.

Raw JSONL is treated as untrusted data. Normalized evidence bounds event count and records process status, messages, commands, tools, searches, file manifests, Git status/diff, and declared checkpoint transitions. Local raw streams should be retained only long enough to diagnose a run and must not be committed. Add `.devquitect-reports/` or another caller-selected evidence directory to local ignore policy when retaining reports.

Adapter, authentication, service, invalid-JSONL, truncated-stream, and missing-terminal-event failures are inconclusive and exit `3`; they never pass and are not automatically retried. Start troubleshooting with `codex --version` and `codex exec --help`, then verify that CLI `0.139.0` exposes the required isolation flags and that model authentication is available only to the trusted subprocess.

## Author behavioral cases

Cases live in `evals/cases/*.yaml`, validate against `schemas/eval-case.schema.json`, and reference a repository fixture under `evals/fixtures/`. Give every case a stable unique ID, fixed repetition count, minimum sandbox, positive or negative activation type, deterministic assertions, forbidden effects, and optional rubric under `evals/rubrics/`.

Use deterministic assertions for filesystem, Git, command/tool, authorization, artifact, structured-output, and checkpoint invariants. Semantic grades address only meaning that cannot be expressed reliably as an observable invariant; they cannot erase a critical failure or missing critical evidence. Do not use exact full-response snapshots as the primary contract.

Ordinary contribution checks remain credential-free:

```text
uv run devquitect validate --source working-tree
uv run pytest
uv run ruff check src tests
```

Trusted maintainers can explicitly execute real behavior with either ChatGPT subscription authentication or an API key:

```text
uv run devquitect eval --source <selector> --suite critical --report .devquitect-reports/critical.json
```

Real behavioral commands default to the lightweight `gpt-5.4-mini` model with reasoning effort
`low`, including both sides of comparisons and `check --behavioral`. This is the normal configuration
for repeated tests. Use `--model` and `--reasoning-effort` only for an intentional calibration or
quality investigation, and review the retained model identity before comparing results.

Exit `3` and `result: inconclusive` identify authentication, service, adapter, or missing-event failures and must be diagnosed rather than retried until pass. Review the source and snapshot identities, case digests, deterministic checks, runtime classification, and redaction labels in the report. A working-tree run remains diagnostic-only. Structural success alone does not publish, install, or make a candidate release-eligible.

## Compare stable N with candidate N+1

Use an immutable commit or promoted reference for stable N and `working-tree` while iterating on N+1:

```text
uv run devquitect compare \
  --stable <stable-commit> \
  --candidate working-tree \
  --suite self-hosting \
  --report .devquitect-reports/self-hosting.json
```

Both selectors are frozen before either run begins. Stable and candidate receive different conversations, workspaces, Codex homes, installed-skill roots, credential copies, and evidence namespaces. Results are classified as `equivalent`, `improvement`, `regression`, `contract-change`, `variable`, or `inconclusive`. A working-tree candidate is always diagnostic-only.

Authorization, routing, persistent-state, or compatibility changes require a reviewed declaration and updated cases. A declaration cannot override a critical safety regression. When stable self-hosting cannot safely author a successor, use manual or external authoring and submit the resulting candidate to the same structural, behavioral, and comparison pipeline; do not bypass gates or evidence requirements.

## Package an exact candidate

Packaging is allowed only from an immutable Git commit whose committed plugin manifest already
contains the requested semantic version. A working-tree selector, mismatched version, missing
declared skill, symlink, archive, cache, report, test input, or machine-local file blocks the
build. The command reads Git objects rather than the checkout and writes only a normalized ZIP
plus a deterministic entry manifest:

```text
uv run devquitect package --source <candidate-commit> --version 0.2.0 --output dist
```

Inspect `dist/devquitect-0.2.0.manifest.json` and the ZIP entry list before release review. Entries
are sorted; timestamps and modes are normalized; the SHA-256 digest binds the archive to the exact
commit and skill snapshot. Rebuilding the same source/version/toolchain must produce the same entry
manifest and artifact digest.

Semantic-version policy treats compatible corrections as patch releases, backward-compatible
behavior or coverage additions as minor releases, and incompatible contract changes as major
releases. Persistent-state schema changes require an explicit migration or recovery case. Reviewed
behavioral deltas need declaration references; critical failures, inconclusive evidence, unsupported
schemas, diagnostic working-tree comparisons, and mismatched snapshot identities remain blockers.

## Propose promotion and recover

After retaining a passing release-eligible evaluation and a clean-commit comparison for the same
snapshot, run:

```text
uv run devquitect release-check \
  --source <candidate-commit> \
  --version 0.2.0 \
  --evidence .devquitect-reports \
  --output dist
```

The release check builds in two fresh roots, requires identical artifacts, validates evidence and
compatibility policy, and emits `devquitect-0.2.0.promotion.json`. Its `approved_by` and
`approved_at` fields remain null: the file is a proposal until a maintainer explicitly approves
promotion. Neither `package` nor `release-check` installs, tags, pushes, publishes, or deploys.

Rollback selects a previously recorded immutable package and its promotion record. Never replace a
published package, rewrite release history, or bypass the same evidence review for a successor.
