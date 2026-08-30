# Devquitect Skill Development System requirements

Status: Approved
Last updated: 2026-08-30

## Confirmed

- Quality must be evaluated through observable behavior and repository effects, not exact response wording.
- Each behavioral scenario must be independent of prior conversation and workspace state.
- Controlled self-hosting must use a stable author version and independently evaluated candidate version.
- Existing skill responsibility and authorization boundaries must remain protected.

## Assumptions

- A single local verification entry point will orchestrate narrower checks.
- Deterministic assertions will be authoritative for structural, filesystem, authorization, and state invariants.
- Semantic grading will be used only for criteria that cannot be expressed reliably as deterministic assertions.

## Open decisions

No requirement decision blocks Gate 1. Numeric thresholds and model/configuration matrices will be established from baseline measurements during technical design and implementation planning.

## Authoring and discovery

- **REQ-001** — The repository shall explain how to create, modify, validate, review, package, and release a skill without requiring undocumented maintainer knowledge.
- **REQ-002** — Every skill shall declare one focused purpose, positive and negative activation boundaries, allowed effects, prohibited effects, and observable completion behavior.
- **REQ-003** — The development system shall validate required skill metadata, directory/name consistency, uniqueness, referenced resources, presentation metadata, and packaging eligibility before behavioral execution.
- **REQ-004** — Routing cases shall verify both prompts that should activate a skill and nearby prompts that must not activate it.

## Behavioral isolation and evidence

- **REQ-005** — Every behavioral case shall start with a fresh conversation and an isolated workspace derived from a declared fixture.
- **REQ-006** — A case shall be able to assert final responses, tool or command activity, filesystem changes, Git changes, persistent-state transitions, and explicitly forbidden effects.
- **REQ-007** — Exact textual matching shall not be required unless the text itself is a formal serialized contract.
- **REQ-008** — Deterministic invariant failures shall not be overridden by a favorable semantic score.
- **REQ-009** — A failed case shall retain enough bounded evidence to diagnose the failure, including case identity, relevant transcript, workspace diff, evaluated version, and grader result.

## Critical workflow protection

- **REQ-010** — Status and review requests declared read-only by a skill shall fail evaluation if they modify the target workspace.
- **REQ-011** — `project-plan-execution` shall fail evaluation if it implements without the required approved persistent definition and explicit slice authorization.
- **REQ-012** — `project-plan-execution` shall not treat implemented work as verified without current executed evidence.
- **REQ-013** — `targeted-refactoring` shall not turn review or planning requests into edits and shall not conceal behavioral change as refactoring.
- **REQ-014** — `software-idea-to-project` shall preserve Gate 1 and Gate 2 approval boundaries and shall not infer implementation authorization from definition work.
- **REQ-015** — Cross-skill tests shall detect responsibility overlap, invalid handoff, lost authorization scope, and incompatible persistent-state expectations.

## Controlled self-hosting

- **REQ-016** — The system shall distinguish the immutable stable author version from the candidate version under evaluation.
- **REQ-017** — Editing a candidate shall not alter the stable skill used by an in-progress authoring or evaluation run.
- **REQ-018** — Every relevant report shall identify the stable source, candidate source, exact source revision, model configuration, fixture, and evaluation time.
- **REQ-019** — Representative scenarios shall be executable independently against stable N and candidate N+1 for behavioral comparison.
- **REQ-020** — Candidate N+1 shall not be its own sole grader, approver, or source of release eligibility.
- **REQ-021** — The suite shall include a self-hosting scenario in which stable `software-idea-to-project` defines an improvement to its successor while preserving approval and implementation boundaries.
- **REQ-022** — A documented recovery path shall permit manual or external authoring when the stable version cannot safely produce a successor, without bypassing candidate validation.

## Packaging and release

- **REQ-023** — The plugin artifact shall be built from an identified source revision using only declared source inputs.
- **REQ-024** — Rebuilding the same version from the same source and compatible toolchain shall produce equivalent package contents.
- **REQ-025** — A candidate shall not be release-eligible while structural checks or critical behavioral invariants fail.
- **REQ-026** — A behavioral contract or persistent schema change shall declare compatibility impact and provide applicable migration or recovery coverage.
- **REQ-027** — Versioning shall distinguish compatible corrections, compatible behavioral additions, and incompatible contract changes.
- **REQ-028** — Promotion evidence shall identify the checks executed, their observed outcomes, accepted behavioral deltas, and residual risk.

## Acceptance scenarios

1. A new contributor can follow repository documentation to add a small skill and run all required local checks.
2. Invalid frontmatter, a name mismatch, duplicate skill names, or a missing reference prevents packaging.
3. A routing change that selects the wrong skill is reported with the triggering prompt and evaluated version.
4. A read-only scenario that writes a file fails regardless of semantic response quality.
5. The runner executes the same scenario against stable and candidate sources without either run sharing state.
6. Modifying the candidate during development does not change the stable author snapshot.
7. A report can prove which exact commit produced the evaluated and packaged candidate.
8. A candidate that relaxes an authorization boundary cannot be promoted without an explicitly accepted contract change and updated tests.
9. A persistent schema change is rejected when no compatible recovery or migration scenario exists.
10. The verified plugin artifact contains the three expected skills and excludes undeclared or machine-local files.

## Quality constraints

- Critical authorization, mutation, and state-integrity invariants require deterministic success in every release-eligibility run.
- Behavioral variability shall be measured through representative repeated cases rather than hidden by broad retry loops.
- Test evidence shall avoid secrets and unnecessarily large raw transcripts.
- The initial system shall remain operable locally without depending on a particular hosted CI provider.
