# Proportional Change Profile

Read this reference for every `system-change` or `hybrid` initiative after enough baseline evidence exists to describe the requested delta. It owns the vocabulary, routing, elevation, approval, and persistence rules for proportional workflow depth. Do not use a Change Profile for `new-system` initiatives.

## Purpose and ownership

A Change Profile is operational routing state, not a generated project artifact. It makes the depth of definition visible and evidence-based without weakening either approval gate or implementation authorization.

In persistent mode, `00-status.md` owns the current profile and `brainstorm.md` records meaningful profile transitions. `01-concept.md` may contain the rationale when it is useful to understand the approved design. Do not create `change-profile.md` inside a project session.

## Profile model

Use these fields:

- `status`: `provisional` or `confirmed`;
- `kinds`: one or more of `bug-fix`, `behavior-change`, `new-capability`, `technical-change`, `migration`, or `deprecation`;
- `impact`: `localized`, `bounded`, `cross-cutting`, or `null` while provisional;
- `workflow_depth`: `expedited`, `standard`, or `full`;
- `affected_surfaces`: any applicable values from `behavior`, `experience`, `domain`, `data`, `interfaces`, `security-privacy`, `operations`, `quality-attributes`, and `migration-compatibility`;
- `elevation_reasons`: current evidence that makes a lower depth unsafe.

Start an applicable initiative as `provisional` with `workflow_depth: standard`, empty kinds and surfaces, null impact, and no elevation reasons. It may start at `full` only when supplied evidence already establishes a full-depth condition.

A confirmed profile requires at least one kind, a non-null impact, at least one affected surface, and enough visible evidence to justify its depth. Keep collection values unique. Historical reasons belong in `brainstorm.md`, not `elevation_reasons`.

## Establish and confirm the profile

Use the relevant System Context, repository evidence, approved documents, and user-supplied facts to establish:

1. current observable behavior and ownership in the affected area;
2. the requested delta;
3. behavior and contracts that must remain unchanged;
4. affected surfaces and trust boundaries;
5. acceptance, verification, rollout, rollback, and compatibility needs;
6. material unknowns or contradictory evidence.

Do not confirm a profile from requested diff size, a feature label, or user preference for speed alone. Missing or stale context does not require documenting the whole repository, but it prevents expedited routing until the affected baseline is sufficiently verified.

## Select workflow depth

Use **expedited** only when every condition below is positively established:

- the profile is confirmed and impact is localized;
- baseline, delta, and preserved behavior are explicit;
- no material product, domain, experience, or technical decision is open;
- acceptance behavior and verification commands or methods are known;
- the current architecture can absorb the change without a material structural decision;
- rollout and rollback are simple and understood.

Any of these conditions disqualifies expedited routing:

- architecture or ownership changes;
- data or state migration;
- authentication, authorization, privacy, sensitive-data, or trust-boundary changes;
- an incompatible public interface, event, storage, or integration contract;
- a new consequential external integration;
- a significant experience change;
- complex rollout, rollback, recovery, concurrency, reliability, or operational risk;
- stale, contradictory, or insufficient evidence in the affected area.

Use **standard** for bounded substantive work that fits established architecture but requires ordinary discovery, design approval, technical confirmation, or planning. A localized impact may still be standard when any expedited precondition is unproven.

Use **full** for cross-cutting, irreversible, migration-heavy, trust-sensitive, compatibility-sensitive, or otherwise high-risk work. `impact: cross-cutting` always implies `workflow_depth: full`; localized file impact never overrides a full-depth risk.

When uncertain, fail safely to standard. Use full when the available evidence positively establishes a full-depth condition.

## Present the profile

Before requesting approval, present a concise profile containing:

- status, kinds, impact, affected surfaces, and selected depth;
- baseline and delta evidence;
- preserved behavior;
- assumptions and open decisions;
- elevation reasons, or an explicit statement that none apply;
- acceptance, verification, and rollback at the depth needed for the decision.

Do not expose empty sections, repeat exhaustive repository inventories, or make the user decode raw checkpoint YAML.

## Apply approval gates

Standard and full initiatives keep the sequential workflow: Gate 1, detailed technical design, Gate 2, then implementation planning.

A confirmed expedited initiative may use one combined approval request only after crystallization includes a bounded no-change architecture assessment. That assessment must establish that existing component ownership, data, interfaces, trust boundaries, operations, and compatibility remain structurally sufficient. It is not detailed technical design and must not invent a proposed architecture.

The combined request must state explicitly that:

- the response approves both Gate 1 and Gate 2;
- the current architecture needs no material change for the confirmed delta;
- approval permits implementation planning only;
- implementation still requires an approved plan and separate slice authorization.

Never infer or self-grant combined approval. If any material architecture treatment is required, elevate to standard or full and use sequential gates.

In persistent mode before a combined request, use `phase: crystallize`, `phase_status: awaiting-approval`, both gates `pending`, null `next_action`, and a `pending_user_action` that names both gates. After explicit approval, mark applicable definition documents approved, mark both gates approved, move directly to active `implementation-planning`, clear the pending action, and continue planning in the same turn.

## Elevate and invalidate safely

Re-evaluate the profile whenever new repository evidence, user input, experience work, architecture work, or planning exposes a wider surface or risk. Elevation is agent-executable and does not require permission to perform the additional analysis, but it must be visible. State the evidence, previous and new depth, affected gates, and next phase.

Use these invalidation rules:

- before approval, update the profile with the normal checkpoint revision;
- after approval, a change confined to technical impact preserves Gate 1 and invalidates Gate 2;
- a material scope, behavior, domain, or experience change invalidates Gate 1 and Gate 2;
- after plan approval, a material profile change returns the plan to `Review`, increments its plan revision, and identifies affected slices.

Do not silently reduce depth, restore invalidated gates, or delete already required analysis. If evidence later supports a lower depth, present and reconfirm the profile; prior approvals remain invalidated until explicitly restored through the applicable gate.

## Preserve cross-skill boundaries

A behavior-preserving localized structural refactor belongs to `targeted-refactoring`. A requested behavior change, capability, migration, deprecation, or architecture initiative belongs here even when its initial file diff appears small.

`project-plan-execution` consumes approved gates, an approved plan, and explicit slice authorization. It does not need to distinguish sequential from combined gate approval, and a Change Profile never authorizes implementation.
