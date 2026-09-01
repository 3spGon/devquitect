# Proportional Change Profile requirements

Status: Approved
Last updated: 2026-08-31

## Confirmed

- Gate 1 was explicitly approved in chat on 2026-08-31.
- The approved scope, preserved behavior, and interaction classification are owned by [01-concept.md](01-concept.md).

## Assumptions

- Semantic behavioral evaluation supplements deterministic safety assertions; it does not replace them.

## Open decisions

No implementation-blocking requirements remain unresolved.

## Functional requirements

- **REQ-001 — Applicability:** The workflow shall use a Change Profile for `system-change` and `hybrid` initiatives and shall not require one for `new-system` initiatives.
- **REQ-002 — Provisional default:** A new applicable profile shall begin `provisional` with `workflow_depth: standard` until repository or approved-document evidence supports confirmation.
- **REQ-003 — Confirmation:** A confirmed profile shall identify at least one change kind, one impact level, and one affected surface, with visible evidence sufficient to justify its depth.
- **REQ-004 — Vocabulary:** Change kinds shall be `bug-fix`, `behavior-change`, `new-capability`, `technical-change`, `migration`, or `deprecation`; impact shall be `localized`, `bounded`, or `cross-cutting`; depth shall be `expedited`, `standard`, or `full`.
- **REQ-005 — Expedited eligibility:** `expedited` shall require a confirmed baseline and delta, localized impact, explicit preserved behavior, no material open decision, known acceptance and verification, and no architecture change, migration, trust-boundary change, incompatible public contract, new consequential external integration, significant experience change, or complex rollout or rollback.
- **REQ-006 — Standard and full routing:** `standard` shall cover bounded substantive work compatible with established architecture. `full` shall cover cross-cutting, irreversible, migration-heavy, trust-sensitive, compatibility-sensitive, or otherwise high-risk work. A localized change may still require `standard` or `full` when a disqualifier applies.
- **REQ-007 — Fail-safe routing:** Missing, stale, contradictory, or insufficient evidence shall prevent `expedited`; uncertainty shall default to `standard` unless confirmed risk requires `full`.
- **REQ-008 — Combined approval:** A confirmed expedited initiative may request one explicit user approval covering Gate 1 and Gate 2 only after presenting the design plus a bounded assessment that the current architecture needs no material change. The skill shall never self-approve either gate.
- **REQ-009 — Sequential approval:** Standard and full initiatives shall preserve the existing sequential Gate 1, technical-design, Gate 2, and planning flow.
- **REQ-010 — Elevation:** New evidence shall elevate depth monotonically from `expedited` to `standard` or `full`, or from `standard` to `full`, and shall present the evidence, previous and new depth, affected gates, and next phase.
- **REQ-011 — Invalidation:** A post-approval technical-impact change shall invalidate Gate 2 while preserving Gate 1 when behavior remains valid. A material scope, behavior, domain, or experience change shall invalidate Gate 1 and Gate 2. A material post-plan profile change shall return the plan to Review and identify affected slices.
- **REQ-012 — Artifact ownership:** Persistent state shall own the operational profile; `01-concept.md` may own its rationale. No numbered or standalone project Change Profile artifact shall be required.
- **REQ-013 — Mode behavior:** Chat-only mode may derive and present a profile but shall not persist it. Persistent mode may store it in the checkpoint after confirmation or material transition.
- **REQ-014 — Compatibility:** The checkpoint shall retain `schema_version: 2`; `change_profile` shall be optional; existing checkpoints without it shall resume without mandatory migration.
- **REQ-015 — System Context:** System Context and repository evidence shall establish the current baseline. Planning alone shall not update System Context; a delivery slice that materially changes the implemented baseline shall refresh it only after implementation and verification.
- **REQ-016 — Downstream execution:** `project-plan-execution` eligibility shall remain based on approved Gate 1, approved Gate 2, an approved plan, and explicit slice authorization, regardless of whether the gates were approved sequentially or together.
- **REQ-017 — Refactoring boundary:** A behavior-preserving localized structural change shall continue to route to `targeted-refactoring`; a behavior change, capability, migration, or architectural initiative shall remain with `software-idea-to-project`.
- **REQ-018 — Neutrality:** The feature shall not reference or depend on Graphify or any other specific skill or external tool.

## Interaction requirements

- **REQ-019 — Profile presentation:** Before requesting approval, the skill shall present status, kinds, impact, affected surfaces, selected depth, supporting evidence, assumptions, and elevation reasons.
- **REQ-020 — Expedited approval wording:** A combined approval request shall state unambiguously that one response approves both Gate 1 and Gate 2 and that it does not authorize implementation.
- **REQ-021 — Elevation feedback:** Elevation shall be visible rather than silently increasing document or analysis depth.
- **REQ-022 — Proportional output:** The skill shall omit empty sections, unnecessary artifacts, and exhaustive repository inventories while retaining enough evidence for safe routing.

## Acceptance scenarios

1. A localized copy or validation correction with a current baseline, preserved behavior, and known tests can be confirmed as expedited and receives one explicit combined gate request.
2. A seemingly small authorization change is not expedited and is elevated to full with the trust-boundary reason visible.
3. A stale or insufficient System Context causes targeted baseline inspection and prevents expedited routing until the affected area is confirmed.
4. A change initially classified as localized is elevated when repository evidence reveals migration, external-contract, or cross-cutting effects; already approved gates are invalidated proportionally.
5. A schema-v2 checkpoint without `change_profile` resumes without migration or failure.
6. Chat-only analysis presents the profile without writing a checkpoint or definition artifact.
7. A behavior-preserving refactor routes to `targeted-refactoring` without creating a software-change session.
8. An expedited combined gate cannot lead to execution without an approved implementation plan and explicit slice authorization.
9. A plan-approved but unimplemented feature is absent from the current System Context.
