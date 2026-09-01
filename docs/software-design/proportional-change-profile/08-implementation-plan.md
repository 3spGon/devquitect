# Proportional Change Profile implementation plan

Status: Approved
Last updated: 2026-08-31
Plan revision: 1

## Confirmed

- Gate 1 and Gate 2 are approved for [01-concept.md](01-concept.md), [02-requirements.md](02-requirements.md), [04-architecture.md](04-architecture.md), [05-data-model.md](05-data-model.md), and [07-decisions.md](07-decisions.md).
- The affected skill is declarative Markdown and YAML under `skills/software-idea-to-project/`.
- Persistent checkpoints currently use schema version 2, and the new field must remain optional.
- Evaluation cases use `schemas/eval-case.schema.json`, cases under `evals/cases/`, deterministic assertions from `src/devquitect_quality/assertions.py`, and optional semantic rubrics under `evals/rubrics/`.
- Changes under `skills/` require relevant positive and negative cases.
- Model-backed evaluation and comparison require separate explicit authorization. Credential-free checks are mandatory after repository changes.
- Current repository HEAD at planning time is `bda8c572efc8d1141692e2bbaaacf214c867b846`; the shared System Context represents an earlier candidate and must not be rewritten during planning.

## Assumptions

- No Python runtime or JSON Schema change is required because the existing case model, rubric resolution, and assertion engine can express the planned evidence.
- `agents/openai.yaml` needs only wording clarification if the final skill behavior is not discoverable from its current description; the public name remains unchanged.

## Open decisions

No implementation-blocking decisions remain.

## Goal and observable outcome

`software-idea-to-project` classifies changes to existing or hybrid systems with a visible, evidence-based Change Profile; selects expedited, standard, or full depth safely; elevates when risk grows; preserves both approval gates and downstream execution authorization; and remains compatible with existing sessions.

## Approved inputs

- [Concept](01-concept.md)
- [Requirements](02-requirements.md)
- [Architecture](04-architecture.md)
- [Data model](05-data-model.md)
- [Decisions](07-decisions.md)
- [Current System Context](../system-context.md)

## Global constraints and non-goals

- Preserve unrelated user changes and existing skill boundaries.
- Do not change session `schema_version: 2`.
- Do not create a project-level Change Profile artifact.
- Do not modify `project-plan-execution` or `targeted-refactoring`.
- Do not add dependencies on Graphify or another named tool or skill.
- Do not run model-backed `eval`, `compare`, or `check --behavioral` without explicit authorization for this task.
- Do not commit, tag, push, package, install, publish, promote, or deploy.
- Keep repository documentation in English while allowing the skill to respond in the user's language.

## Delivery slices

### SLICE-001 — Implement proportional Change Profile routing end to end

**Outcome:** A maintainer can use `software-idea-to-project` for a new system exactly as before, while existing-system and hybrid initiatives receive a compatible, persistent, proportional profile with safe routing, elevation, and approval behavior.

**Dependencies:** Approved Gate 1 and Gate 2 artifacts. No code or external dependency prerequisite.

**Files:**

- Create verified proposed path `skills/software-idea-to-project/references/change-profile.md`.
- Modify verified paths:
  - `skills/software-idea-to-project/SKILL.md`
  - `skills/software-idea-to-project/references/discovery.md`
  - `skills/software-idea-to-project/references/session-state.md`
  - `skills/software-idea-to-project/references/artifacts.md`
  - `skills/software-idea-to-project/references/experience-design.md`
  - `skills/software-idea-to-project/references/technical-design.md`
  - `skills/software-idea-to-project/references/implementation-planning.md`
  - `skills/software-idea-to-project/agents/openai.yaml` only if needed to expose proportional change handling accurately.
- Add focused versioned cases under `evals/cases/` for expedited eligibility, trust-sensitive elevation, stale baseline behavior, legacy checkpoint compatibility, and behavior-preserving refactor routing.
- Add `evals/rubrics/change-profile-routing.yaml` with semantic dimensions for correct profile evidence, proportional depth, combined approval wording, elevation transparency, and preservation of implementation authorization.
- Modify `tests/unit/test_cases.py` to require the new compatibility and routing coverage by stable case ID.
- Refresh `docs/software-design/system-context.md` only after the implemented skill and focused credential-free tests pass.

**Interfaces and rules implemented:**

- Add the `change_profile` checkpoint shape and invariants from [05-data-model.md](05-data-model.md).
- Make `references/change-profile.md` the sole normative owner of lifecycle, eligibility, disqualifiers, elevation, invalidation, and combined approval.
- Initialize applicable new profiles as provisional and standard; omit the field for new-system initiatives; interpret legacy absence without migration.
- Require positive evidence before expedited routing and fail closed to standard or full.
- Keep the expedited flow in crystallization until one explicit combined approval marks both gates approved; never infer or self-grant approval.
- Preserve sequential gates for standard and full work.
- Show all elevation evidence and invalidate only dependent gates.
- Keep the current baseline distinct from proposed behavior and schedule System Context refresh only after verification.
- Preserve `project-plan-execution` eligibility and `targeted-refactoring` routing without editing either skill.

**Acceptance and focused test cases:**

- A localized, well-evidenced change is presented as confirmed expedited and requests explicit combined Gate 1 and Gate 2 approval without implementation authorization.
- A change affecting authentication or authorization elevates to full even when its file diff appears small.
- Missing or stale relevant context prevents expedited routing and triggers proportional baseline inspection.
- A schema-v2 checkpoint without `change_profile` remains valid and is not rewritten during status-only handling.
- A behavior-preserving structural refactor routes to `targeted-refactoring`.
- Existing `gate-one-bypass`, `cross-skill-handoff`, `software-idea-positive`, `software-idea-negative`, and `self-hosting` cases remain structurally valid and preserve their safety effects.
- The unit case test fails if any required Change Profile case is missing or duplicated.

Credential-free verification commands:

```text
uv run pytest tests/unit/test_cases.py tests/integration/test_eval_command.py
uv run devquitect check --source working-tree --report .devquitect-reports/check.json
uv run ruff check src tests
git diff --check
```

Expected signal: every command exits `0`; the check report has `result: pass`; no structural case, reference, checkpoint, or lint failure is reported.

Behavioral verification, only after separate explicit authorization:

```text
uv run devquitect eval --source working-tree --suite change-profile --model gpt-5.4-mini --reasoning-effort low --report .devquitect-reports/change-profile.json
```

Expected signal: exit `0`, every focused case passes, no critical forbidden effect occurs, and the working-tree evidence remains diagnostic-only. If behavioral comparison is later needed for promotion, use an immutable stable selector and a separately reviewed compatibility declaration; that release workflow is not authorized by this slice.

**Documentation, compatibility, rollback, and evidence:**

- After implementation and credential-free verification, refresh System Context `Current capabilities`, `Core workflows` if present, `Preserved behavior`, `Known limitations and context gaps`, and `Authoritative references` to describe the implemented Change Profile contract. Use an explicit working-tree baseline reference until an immutable candidate commit is separately authorized; never invent a commit or describe unverified behavior as current.
- Record the exact modified paths, commands, exit codes, focused case IDs, and report result in the delivery checkpoint created by `project-plan-execution`.
- Rollback consists of reverting only this slice's skill, case, rubric, test, and System Context edits. Existing checkpoints remain readable because the added field is optional and no migration occurs.
- Do not modify the completed `skill-development-system` definition or delivery checkpoints.

## Traceability matrix

| Requirement | Delivery | Verification |
| --- | --- | --- |
| REQ-001–REQ-007 | SLICE-001 profile reference, discovery, orchestrator | expedited, elevation, and stale-baseline cases |
| REQ-008–REQ-011 | SLICE-001 gate and checkpoint transitions | combined-approval, gate-bypass, and elevation cases |
| REQ-012–REQ-015 | SLICE-001 artifact, state, planning, and baseline integration | structural check, legacy checkpoint case, System Context diff review |
| REQ-016–REQ-018 | SLICE-001 preserved cross-skill contracts | cross-skill handoff and refactor-routing cases |
| REQ-019–REQ-022 | SLICE-001 presentation rules and rubric | change-profile semantic rubric plus deterministic forbidden effects |

## Residual risks

- Semantic evaluation can vary by model; deterministic authorization and write-safety checks remain dominant.
- A single profile vocabulary cannot encode every domain risk. The explicit elevation reasons and full-depth fallback preserve safety when categories are insufficient.
- The first version assumes one primary system per repository; specialized monorepo routing remains deferred.

## Final readiness review

- Every approved requirement maps to SLICE-001 and a verification method.
- Exact existing paths and credential-free commands were verified from repository evidence; the one new reference and new case/rubric files are clearly identified as proposed.
- No placeholder, migration, external dependency, or hidden implementation decision remains.
- Compatibility and rollback are explicit.
- The shared System Context refresh occurs only after implementation and verification within the slice.

Implementation requires separate authorization for the concrete slice `SLICE-001`. Plan approval alone does not authorize repository implementation.
