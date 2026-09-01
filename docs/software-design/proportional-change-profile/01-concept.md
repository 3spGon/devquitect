# Proportional Change Profile concept

Status: Approved
Last updated: 2026-08-31

## Confirmed

- The initiative changes the existing `software-idea-to-project` skill.
- Gate 1 was explicitly approved in chat on 2026-08-31.
- The current skill distinguishes `new-system`, `system-change`, and `hybrid`, but it does not own a structured mechanism for choosing proportional workflow depth within changes to existing systems.
- The public skill name remains Software Idea to Project.

## Assumptions

- Repository-owned skill and definition documents continue using English to match the established repository convention. The skill may communicate with users in their language.
- One primary system per repository remains the supported System Context model.

## Open decisions

No implementation-blocking product decisions remain.

## Problem

A request that changes existing software may be a localized correction, a bounded feature, or a cross-cutting migration. Treating them identically either adds unnecessary ceremony to safe changes or under-analyzes consequential ones. The workflow needs a visible, evidence-based profile that selects the minimum safe depth and grows when new evidence increases risk.

## Desired outcome

For every `system-change` or `hybrid` initiative, the skill establishes a provisional Change Profile, confirms it from the relevant baseline and requested delta, and routes the initiative through an expedited, standard, or full workflow without weakening approval or implementation-authorization boundaries.

## Baseline and requested delta

Current behavior:

- the skill reconstructs a proportional baseline for existing systems;
- Gate 1 precedes detailed architecture;
- Gate 2 precedes implementation planning;
- persistent sessions use schema-v2 checkpoints;
- System Context represents current implemented behavior, not planned behavior.

Requested delta:

- add an explicit structured Change Profile;
- make workflow depth observable and justified;
- support a tightly constrained expedited path with explicit combined Gate 1 and Gate 2 approval;
- elevate automatically when evidence reveals wider impact or risk;
- preserve compatibility with existing sessions and downstream execution.

## Preserved behavior

- The skill remains a definition workflow and never infers implementation authorization.
- Gate 1 and Gate 2 remain mandatory user approvals.
- `08-implementation-plan.md` remains required for persistent execution.
- System Context is not updated with planned behavior.
- Chat-only mode does not write files.
- Existing schema-v2 sessions remain valid without migration.
- Behavior-preserving localized refactors remain owned by `targeted-refactoring`.

## Scope

- Change Profile vocabulary, state, confirmation, routing, elevation, and invalidation.
- Proportional artifact and interaction guidance.
- Persistent checkpoint compatibility.
- Evaluation cases covering positive, negative, safety, and cross-skill boundaries.

## Non-goals

- A generated `change-profile.md` project artifact.
- Changes to `project-plan-execution` or `targeted-refactoring`.
- Dependencies on Graphify or any named external skill or tool.
- Monorepo-specific multi-system context modeling.
- Implementation, packaging, release, installation, or publication as part of this definition workflow.

## Interaction surface

The interaction surface is **minimal**. The skill must present the confirmed profile, its evidence, the selected depth, any elevation, and the exact approval effect in concise text. There is no graphical or visual-design surface, so a separate experience artifact is not warranted.
