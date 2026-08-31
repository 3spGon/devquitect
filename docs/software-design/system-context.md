---
schema_version: 1
document: system-context
system: Devquitect
scope: repository
lifecycle: in-development
context_status: current
revision: 7
last_updated: 2026-08-30
baseline_reference: candidate@5f258930bfada1702906fcc367d14a473168ee80
---

# Devquitect system context

## Quick orientation

Devquitect is a Git repository containing three related Codex skills that cover software definition, approved plan execution, and targeted behavior-preserving refactoring. Repository-owned Python tooling freezes skills into isolated snapshots, validates their structure offline, and runs versioned behavioral cases through an isolated Codex CLI adapter.

## Purpose

The current system provides reusable agent workflows for moving from a software idea or change request to an approved technical definition, executing an explicitly authorized persistent plan, and performing narrowly scoped refactors without changing intended behavior.

## Current lifecycle

The repository is in development. A preliminary `v0.1.0` tag exists, and exact commit `5f258930bfada1702906fcc367d14a473168ee80` carries the unpromoted `0.2.0` plugin manifest. The skill set and its shared workflow contracts continue to evolve.

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

- continuous integration;
- public plugin distribution;
- automated release publication;
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
- `devquitect eval` loads schema-valid YAML cases, creates a fresh Git workspace, conversation, Codex home, skill root, and evidence namespace per attempt, and emits canonical evaluation reports.
- Deterministic assertions dominate optional semantic grades; critical failures cannot be overridden and infrastructure failures remain inconclusive with exit `3`.
- Trusted local evaluation can scope an existing ChatGPT login cache to one isolated subprocess without retaining credentials in fixtures, reports, or repository files.
- `devquitect compare` freezes stable and candidate sources before execution, runs them independently, and classifies equivalent behavior, improvement, regression, reviewed contract change, variability, or inconclusive infrastructure.
- `devquitect package` reads an exact Git commit, enforces the committed semantic version and package allowlist, and emits a normalized plugin ZIP with entry and artifact SHA-256 identities.
- `devquitect release-check` rebuilds in two fresh roots, binds passing behavioral evidence to the same snapshot, applies compatibility and migration policy, and emits an explicitly unapproved promotion proposal.
- `devquitect check` composes structural validation with the credential-free unit, integration, and CLI contract suite; `--behavioral` explicitly adds trusted critical evaluation and clean-ref self-hosting comparison.
- Real behavioral commands default to the efficient `gpt-5.6-luna` model at `low` reasoning effort, retain that identity in evidence, and allow explicit calibration overrides; fast checks invoke no model.

## Technical landscape

The maintained skills remain declarative Markdown and YAML. Repository quality tooling uses Python 3.12 with a `src/` package layout, setuptools build metadata, a `uv.lock` dependency lock, PyYAML, jsonschema, pytest, and Ruff. Implemented components own source selection, read-only snapshots, structural validation, isolated Codex execution, normalized observations, deterministic assertions, behavioral cases, stable/candidate comparison, deterministic packaging, release-eligibility policy, canonical reporting, and the `devquitect` plugin definition. Publication remains manual and outside the tooling.

## Development and verification

The stable baseline and source-snapshot component are verified with:

```text
uv sync --all-groups
uv run pytest
uv run devquitect validate --source working-tree --format json
uv run ruff check src tests
git diff --exit-code -- skills
```

The 58-test fast suite verifies immutable reconstruction, source eligibility, post-freeze isolation, invalid source/path handling, structural records, report safety, fresh attempt boundaries, JSONL normalization, redaction, deterministic precedence, case contracts, paired snapshots, comparison policy, semantic-version policy, lightweight behavioral defaults, package allowlists, normalized rebuilds, release evidence blocking, and integrated check exit/report behavior. A trusted critical run passed seven isolated stable cases, and a trusted self-hosting comparison classified stable and clean candidate commit `5f25893` as equivalent and release-eligible. The full behavioral `check` passed against that exact snapshot. The `0.2.0` package rebuilt with digest `sha256:ce15c1cfb1966c69ebca32bfed9fbfcdbe41a1a054844360f70f90a026eeb5ba`; the promotion record remains an unapproved proposal.

## Preserved behavior

Future initiatives must preserve the distinct responsibility boundaries among software definition, authorized delivery, and targeted refactoring. They must not silently broaden implementation authority, conflate implemented work with verified work, or turn read-only requests into repository mutations.

## Known limitations and context gaps

- Contributor checks remain local because no hosted CI provider is configured.
- Behavioral checks require an explicit trusted run with ChatGPT or API authentication; ordinary fast checks remain credential-free.
- Compatibility across model or Codex runtime changes is not measured.
- No marketplace entry, installation automation, hosted CI, or publication mechanism has been implemented.
- The current source-snapshot implementation is verified in the working tree but has not been committed or promoted as a release.

## Authoritative references

- [`software-idea-to-project`](../../skills/software-idea-to-project/SKILL.md)
- [`project-plan-execution`](../../skills/project-plan-execution/SKILL.md)
- [`targeted-refactoring`](../../skills/targeted-refactoring/SKILL.md)
- [Stable N manifest](../../baselines/stable-n.json)
- [Source snapshot implementation](../../src/devquitect_quality/sources.py)
- [Structural validator](../../src/devquitect_quality/validate.py)
- [Behavioral adapter](../../src/devquitect_quality/codex_adapter.py)
- [Behavioral cases](../../evals/cases)
- [Comparison engine](../../src/devquitect_quality/comparison.py)
- [Plugin packager](../../src/devquitect_quality/packaging.py)
- [Promotion policy](../../src/devquitect_quality/promotion.py)
- [Contributor guidance](../../docs/contributing-skills.md)
- [Repository README](../../README.md)
- [Snapshot tests](../../tests/integration/test_stable_baseline.py)
