---
schema_version: 1
document: system-context
system: Devquitect
scope: repository
lifecycle: in-development
context_status: current
revision: 2
last_updated: 2026-08-30
baseline_reference: working-tree@264f4648ae1e699168347eb8e5945459bfbd0e27
---

# Devquitect system context

## Quick orientation

Devquitect is a Git repository containing three related Codex skills that cover software definition, approved plan execution, and targeted behavior-preserving refactoring. It now also contains the verified Python foundation for freezing those skills from Git or a working tree into isolated, content-addressed snapshots and an immutable stable N baseline record.

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
- the Python toolchain and focused snapshot tests declared by `pyproject.toml` and `uv.lock`.

Outside the current implemented baseline:

- automated structural validation;
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

## Technical landscape

The maintained skills remain declarative Markdown and YAML. Repository quality tooling now uses Python 3.12 with a `src/` package layout, setuptools build metadata, a `uv.lock` dependency lock, pytest, and Ruff. The first implemented component owns source selection, safe Git/worktree enumeration, symlink/path validation, read-only materialization, and content manifests. No plugin manifest, behavioral runner, structural-validator command, or release pipeline exists yet.

## Development and verification

The stable baseline and source-snapshot component are verified with:

```text
uv sync --all-groups
uv run pytest tests/unit/test_sources.py tests/integration/test_stable_baseline.py
uv run ruff check src tests
git diff --exit-code -- skills
```

The focused suite verifies immutable reconstruction from the recorded commit, stable-versus-working-tree eligibility, post-freeze isolation, unsafe symlink rejection, invalid source handling, and the exact three-skill baseline. Structural skill validation, routing and behavioral invariants, and packaging checks remain future slices.

## Preserved behavior

Future initiatives must preserve the distinct responsibility boundaries among software definition, authorized delivery, and targeted refactoring. They must not silently broaden implementation authority, conflate implemented work with verified work, or turn read-only requests into repository mutations.

## Known limitations and context gaps

- There is no contributor-facing project documentation or definition of done.
- Structural and behavioral skill regressions are not yet automatically detected.
- Release artifacts are not built reproducibly from a verified commit.
- Compatibility across model or Codex runtime changes is not measured.
- A distribution mechanism for the three-skill bundle has not been implemented.
- The current source-snapshot implementation is verified in the working tree but has not been committed or promoted as a release.

## Authoritative references

- [`software-idea-to-project`](../../skills/software-idea-to-project/SKILL.md)
- [`project-plan-execution`](../../skills/project-plan-execution/SKILL.md)
- [`targeted-refactoring`](../../skills/targeted-refactoring/SKILL.md)
- [Stable N manifest](../../baselines/stable-n.json)
- [Source snapshot implementation](../../src/devquitect_quality/sources.py)
- [Snapshot tests](../../tests/integration/test_stable_baseline.py)
