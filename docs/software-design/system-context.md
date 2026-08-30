---
schema_version: 1
document: system-context
system: Devquitect
scope: repository
lifecycle: in-development
context_status: current
revision: 3
last_updated: 2026-08-30
baseline_reference: working-tree@264f4648ae1e699168347eb8e5945459bfbd0e27
---

# Devquitect system context

## Quick orientation

Devquitect is a Git repository containing three related Codex skills that cover software definition, approved plan execution, and targeted behavior-preserving refactoring. Repository-owned Python tooling now freezes those skills into isolated snapshots and validates their structure, metadata, schemas, references, and plugin inputs offline.

## Purpose

The current system provides reusable agent workflows for moving from a software idea or change request to an approved technical definition, executing an explicitly authorized persistent plan, and performing narrowly scoped refactors without changing intended behavior.

## Current lifecycle

The repository is in development. A preliminary `v0.1.0` tag exists, while the skill set and its shared workflow contracts continue to evolve.

## System boundaries

Inside the current system:

- skill instructions under `skills/*/SKILL.md`;
- supporting workflow references under each skill's `references/` directory;
- optional Codex presentation and invocation metadata under `agents/openai.yaml`.
- Python source-snapshot records and materialization under `src/devquitect_quality/`;
- the stable N provenance manifest under `baselines/stable-n.json`;
- the Python toolchain and focused snapshot tests declared by `pyproject.toml` and `uv.lock`;
- the `devquitect` plugin definition under `.codex-plugin/plugin.json`;
- versioned validation schemas under `schemas/` and contributor guidance under `docs/`.

Outside the current implemented baseline:

- behavioral evaluation infrastructure and isolated fixtures;
- continuous integration;
- plugin packaging and public distribution;
- automated release production;
- MCP servers, connectors, applications, or graphical interfaces.

## Actors and external systems

- Skill maintainers and contributors author and review the repository content.
- Codex loads and follows the skill instructions when a request explicitly or implicitly selects them.
- Git records the source history and the `v0.1.0` preliminary release marker.

No Git remote or CI provider is configured in the represented baseline.

## Current capabilities

- `software-idea-to-project` defines new systems and software changes through approval gates and can preserve cross-session state in a target repository.
- `project-plan-execution` executes authorized slices from an approved persistent plan and records current verification evidence.
- `targeted-refactoring` assesses, plans, executes, or reviews bounded behavior-preserving refactors.
- The skills use progressive disclosure through directly referenced Markdown files.
- Each skill includes user-facing metadata in `agents/openai.yaml`.
- Stable N is identified by commit `264f4648ae1e699168347eb8e5945459bfbd0e27` and aggregate snapshot digest `sha256:062d5509956e73de366b9c351bb93441dcd39e2bf04cc8b6b870f797717960ef`.
- Git refs and working-tree skill sources can be copied into separate read-only snapshots with normalized file, skill, and aggregate SHA-256 identities.
- Git-ref snapshots are eligible stable sources; working-tree snapshots are always diagnostic-only, even when their skill files are clean.
- `devquitect validate --source <selector>` checks frontmatter, name consistency and uniqueness, local references, presentation metadata, schema compatibility, plugin membership, and package allowlists without credentials or network access.
- Validation emits the approved JSON report envelope, an equivalent text presentation, normalized relative paths, atomic report files, and stable exit codes `0`, `1`, and `2`.

## Technical landscape

The maintained skills remain declarative Markdown and YAML. Repository quality tooling uses Python 3.12 with a `src/` package layout, setuptools build metadata, a `uv.lock` dependency lock, PyYAML, jsonschema, pytest, and Ruff. Implemented components own source selection, read-only snapshots, structural validation, canonical reporting, and the `devquitect` plugin definition. No behavioral runner, comparison engine, reproducible package builder, or release pipeline exists yet.

## Development and verification

The stable baseline and source-snapshot component are verified with:

```text
uv sync --all-groups
uv run pytest
uv run devquitect validate --source working-tree --format json
uv run ruff check src tests
git diff --exit-code -- skills
```

The suite verifies immutable reconstruction from the recorded commit; stable-versus-working-tree eligibility; post-freeze isolation; invalid source and unsafe path handling; valid current skill/plugin inputs; specific malformed metadata, duplicate-name, missing-reference, unsupported-schema, and unexpected-file records; report-path normalization; and atomic report replacement. Routing, behavioral invariants, comparisons, and reproducible packaging remain future slices.

## Preserved behavior

Future initiatives must preserve the distinct responsibility boundaries among software definition, authorized delivery, and targeted refactoring. They must not silently broaden implementation authority, conflate implemented work with verified work, or turn read-only requests into repository mutations.

## Known limitations and context gaps

- Contributor guidance currently covers structural authoring and validation only; the integrated definition of done remains a later slice.
- Structural regressions are detected locally, but behavioral skill regressions are not yet automatically detected.
- Release artifacts are not built reproducibly from a verified commit.
- Compatibility across model or Codex runtime changes is not measured.
- The plugin is defined but no reproducible archive, marketplace entry, installation, or publication mechanism has been implemented.
- The current source-snapshot implementation is verified in the working tree but has not been committed or promoted as a release.

## Authoritative references

- [`software-idea-to-project`](../../skills/software-idea-to-project/SKILL.md)
- [`project-plan-execution`](../../skills/project-plan-execution/SKILL.md)
- [`targeted-refactoring`](../../skills/targeted-refactoring/SKILL.md)
- [Stable N manifest](../../baselines/stable-n.json)
- [Source snapshot implementation](../../src/devquitect_quality/sources.py)
- [Structural validator](../../src/devquitect_quality/validate.py)
- [Contributor guidance](../../docs/contributing-skills.md)
- [Snapshot tests](../../tests/integration/test_stable_baseline.py)
