# Devquitect Next implementation plan

Status: Approved
Plan revision: 2
Last updated: 2026-09-22

## Goal

Deliver lean and traceable skill contracts plus QUICK in 0.7.0; generalized definition continuity and invocation policy in 0.8.0; then evidence-backed stabilization in 1.0.0. `verify_slice.py`, its Python/PyYAML dependencies, YAML inventory, and acceptance behavior are excluded from every slice.

## Approved inputs and constraints

- [Concept](01-concept.md), [requirements](02-requirements.md), [architecture](04-architecture.md), [data model](05-data-model.md), [interfaces](06-api-contracts.md), [decisions](07-decisions.md), and [prompt-change ledger](prompt-change-ledger.md).
- Preserve the three established authority boundaries. Do not introduce a fourth global router.
- Each material prompt change is one named group, with an immutable baseline, the same deterministic cases, and a ledger entry. Behavioral comparison is separately authorized and never substitutes for deterministic failures.
- Do not modify `skills/project-plan-execution/scripts/verify_slice.py`, its YAML inventory contract, or its dependencies.
- No slice is authorized by this plan. Approval must name the intended `SLICE-DN-*` identifiers.

## Revision 2 review impact

Gate 1 and Gate 2 approved the expanded definition and cross-generation matrix. Plan revision 2 updates `SLICE-DN-004` with the approved model IDs and evidence criteria. The plan remains in Review pending explicit plan approval; no implementation slice is authorized.

## SLICE-DN-001 — Lean entrypoints and prompt-change evidence for 0.7.0

Simplify the three existing skill entrypoints so each policy appears once while their authoritative references retain detailed mechanics. Establish the append-only prompt-change ledger and deterministic positive/negative cases for every changed rule group.

Paths: `skills/software-idea-to-project/`, `skills/project-plan-execution/`, `skills/targeted-refactoring/`, `authority-map.yaml`, `evals/cases/`, `docs/skill-change-ledger.md` (new), and `docs/software-design/devquitect-next/prompt-change-ledger.md`.

Outcome: concise entrypoints preserve definition-versus-implementation, plan-execution, and behavior-preserving-refactor boundaries, with reconstructable source and evidence for each simplification.

## SLICE-DN-002 — QUICK route for 0.7.0

Add `quick-change` as an independently discoverable skill for authorized, localized, reversible, directly verifiable work. Its description and deterministic cases distinguish eligible work from mandatory escalation; explicit invocation remains authoritative.

Paths: `skills/quick-change/` (new), `.codex-plugin/plugin.json`, `authority-map.yaml`, and `evals/cases/`.

Outcome: an eligible local change can use QUICK without a universal router, while features, public contracts, persistence, security, migrations, multi-module work, and durable continuity are routed away.

## SLICE-DN-003 — General workflow depth and durable roots for 0.8.0

Generalize workflow-depth selection beyond system-change sessions and add the minimal persistent-state contract for a caller-supplied repository-relative definition root. Preserve legacy session discovery and do not move existing sessions.

Paths: `skills/software-idea-to-project/SKILL.md`, `skills/software-idea-to-project/references/` (including new `workflow-depth.md`), `authority-map.yaml`, and `evals/cases/`.

Outcome: every initiative has proportionate depth, and a resumed persistent session uses its recorded root before default discovery; ambiguous candidates require user selection.

## SLICE-DN-004 — Invocation policy and evaluation matrix for 0.8.0

Declare per-skill implicit-invocation policy in metadata: definition, QUICK, and targeted refactoring may be eligible; `project-plan-execution` is explicit-only. Add the cross-generation model/host matrix and ledger references needed to make the approved GPT-5.6 baseline and GPT-6 Sol/Luna comparisons reproducible without pooling results.

Paths: `skills/*/agents/openai.yaml`, `skills/software-idea-to-project/references/`, `skills/quick-change/`, `authority-map.yaml`, `evals/cases/`, `docs/skill-change-ledger.md`, and `docs/software-design/devquitect-next/prompt-change-ledger.md`.

Outcome: host routing has explicit boundaries, and each behavioral evidence row identifies one canonical model ID, host, runtime, reasoning effort where supported, suite revision, repetitions, report references, and an independent verdict. The initial rows are `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-6-sol`, and `gpt-6-luna`. Comparisons reuse the same prompt-change group and representative cases. If host, runtime, or effort differs, record it and avoid a model-only claim. This slice runs no behavioral comparison without separate user authorization.

## SLICE-DN-005 — Stabilize the changed contracts for 1.0.0

Run the credential-free evidence suite against the assembled candidate, close deterministic gaps in the changed skill contracts, and confirm the delivered diff did not alter `verify_slice` or its verification inventory contract.

Paths: changed `skills/`, `authority-map.yaml`, `evals/cases/`, `.codex-plugin/plugin.json`, and `docs/software-design/system-context.md`.

Outcome: 1.0.0 eligibility has current deterministic evidence for entrypoint boundaries, QUICK escalation, workflow continuity, invocation policy, ledger completeness, and the preserved verifier boundary.

## SLICE-DN-006 — Release-readiness evidence for 1.0.0

Bind release-readiness evidence to the exact candidate source, refresh the System Context only from verified implementation evidence, and document any authorized behavioral rows without publishing, tagging, or promoting a release.

Paths: `.devquitect-reports/`, `docs/software-design/system-context.md`, `docs/skill-change-ledger.md`, `.codex-plugin/plugin.json`, and changed skill documentation.

Outcome: maintainers can decide separately whether to publish 1.0.0 from current, attributable evidence.

## Verification inventory

```devquitect-verification
schema_version: 1
slices:
  SLICE-DN-001:
    depends_on: []
    criteria:
      AC-DN-001:
        text: "The three lean entrypoints preserve their distinct authority boundaries and every material rule-group change has an immutable baseline and ledger entry."
        requirement: R-01
      AC-DN-002:
        text: "Each changed entrypoint rule group has relevant deterministic positive and negative coverage."
        requirement: R-02
    checks:
      CHECK-DN-001:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-002:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-003:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills/software-idea-to-project"
      - "skills/project-plan-execution"
      - "skills/targeted-refactoring"
      - "authority-map.yaml"
      - "evals/cases"
      - "docs/skill-change-ledger.md"
  SLICE-DN-002:
    depends_on: ["SLICE-DN-001"]
    criteria:
      AC-DN-003:
        text: "QUICK is independently discoverable for eligible local changes and escalates every stated disqualifier."
        requirement: R-03
      AC-DN-004:
        text: "QUICK does not introduce a universal fourth routing skill."
        requirement: R-04
    checks:
      CHECK-DN-004:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-005:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-006:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills/quick-change"
      - ".codex-plugin/plugin.json"
      - "authority-map.yaml"
      - "evals/cases"
  SLICE-DN-003:
    depends_on: ["SLICE-DN-002"]
    criteria:
      AC-DN-005:
        text: "Workflow depth is recorded for every initiative, legacy sessions default safely, and configured roots resume without moving existing sessions."
        requirement: R-09
      AC-DN-006:
        text: "Ambiguous persistent-session discovery requires user selection."
        requirement: R-09
    checks:
      CHECK-DN-007:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-008:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-009:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills/software-idea-to-project"
      - "authority-map.yaml"
      - "evals/cases"
  SLICE-DN-004:
    depends_on: ["SLICE-DN-003"]
    criteria:
      AC-DN-007:
        text: "project-plan-execution is explicit-only while other skill policies are declared, and explicit invocation takes precedence."
        requirement: R-10
      AC-DN-008:
        text: "Each authorized behavioral evidence row records one canonical model ID, host, runtime, reasoning effort where supported, suite revision, repetitions, report references, and an independent verdict; the initial model IDs are gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna, gpt-6-sol, and gpt-6-luna, compared on the same prompt-change group and representative cases without pooling results."
        requirement: R-10
    checks:
      CHECK-DN-010:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-011:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-012:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills"
      - "authority-map.yaml"
      - "evals/cases"
      - "docs/skill-change-ledger.md"
  SLICE-DN-005:
    depends_on: ["SLICE-DN-004"]
    criteria:
      AC-DN-009:
        text: "The assembled candidate has current credential-free evidence for changed contracts and leaves verify_slice.py and its YAML verification contract unchanged."
        requirement: R-05
      AC-DN-010:
        text: "The System Context reflects only verified implementation evidence."
        requirement: R-06
    checks:
      CHECK-DN-013:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-014:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-015:
        command: "git diff --check"
        cwd: "."
    inputs:
      - "skills"
      - "authority-map.yaml"
      - "evals/cases"
      - "docs/software-design/system-context.md"
  SLICE-DN-006:
    depends_on: ["SLICE-DN-005"]
    criteria:
      AC-DN-011:
        text: "Release-readiness evidence is bound to an exact candidate and does not publish, tag, or promote it."
        requirement: R-06
      AC-DN-012:
        text: "Authorized behavioral evidence, if present, does not override deterministic failures or combine independent matrix rows."
        requirement: R-10
    checks:
      CHECK-DN-016:
        command: "uv run devquitect check --source working-tree --report .devquitect-reports/check.json"
        cwd: "."
      CHECK-DN-017:
        command: "uv run ruff check src tests"
        cwd: "."
      CHECK-DN-018:
        command: "git diff --check"
        cwd: "."
    inputs:
      - ".devquitect-reports"
      - "docs/software-design/system-context.md"
      - "docs/skill-change-ledger.md"
      - ".codex-plugin/plugin.json"
```

## Rollout and rollback

Each 0.7.0 and 0.8.0 slice is reverted by restoring only its changed skill and contract files. Existing sessions remain in place. `verify_slice.py` is never part of this rollout. 1.0.0 readiness does not tag, publish, or promote; those actions require separate authorization.
