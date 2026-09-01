# Persistent Artifacts

Read this reference when the user chooses persistent workspace, requests definition files, or resumes an existing session. Also read [session-state.md](session-state.md) whenever durable workflow state is created, queried, repaired, or updated.

## Session directory

Store each definition under:

```text
docs/software-design/<slug>/
```

Derive `<slug>` from an explicit project name or, if none exists, a concise topic name. Use lowercase ASCII letters, digits, and hyphens. Ask only when two plausible names would create meaningfully different session identities.

Before creating the directory, inspect `docs/software-design/` for a matching or clearly related session. Treat `00-status.md` as the entry point when present. If a related session exists, summarize its workflow state and ask whether to resume it or use a distinct slug. Never overwrite or reset an existing session without explicit direction.

## Shared system context

`docs/software-design/system-context.md` is the optional shared orientation and current-baseline document for the repository's primary system. Read [system-context.md](system-context.md) before creating, refreshing, or relying on it.

It belongs to the system rather than a definition session. Do not place it inside a session directory, assign it a numbered artifact slot, list it in a session's `artifacts` map, or apply the canonical `Draft | Review | Approved` header. Its own lifecycle, freshness, revision, and authority contract are defined in the reference above. It does not participate directly in Gate 1 or Gate 2.

## Artifact set

Create `00-status.md` and `brainstorm.md` when persistent mode begins. The checkpoint is mandatory; canonical definition documents remain conditional:

| Artifact | Create when |
| --- | --- |
| `00-status.md` | Always create for persistent mode; it is the durable workflow checkpoint. |
| `01-concept.md` | Purpose, actors, outcomes, boundaries, or non-goals need a canonical definition. |
| `02-requirements.md` | Workflows, scenarios, constraints, or acceptance criteria are substantive. |
| `03-domain.md` | Domain concepts, rules, identities, ownership, or states affect behavior. |
| `experience-design.md` | Human tasks, flows, views, states, navigation, accessibility, responsive behavior, or design-system decisions need a canonical owner. |
| `04-architecture.md` | Multiple components, dependencies, or structural choices require explanation. |
| `05-data-model.md` | Persistence, relationships, lifecycle, querying, or migration matters. |
| `06-api-contracts.md` | APIs, commands, events, webhooks, or integration contracts must be shared. |
| `07-decisions.md` | Consequential alternatives and their rationale need durable records. |
| `08-implementation-plan.md` | Gate 2 is approved and an executable delivery plan is requested. |
| `09-delivery-status.md` | `$project-plan-execution` initializes authorized implementation from an approved plan. |

Do not create empty files, placeholder sections, or every artifact by default. If one concise document is sufficient, use it.

## Authority and evolution

`00-status.md` is authoritative for definition workflow phase, phase status, gates, next action, and handoff context. Follow [session-state.md](session-state.md) for its schema, update ordering, recovery, and single-writer rules. When present, `09-delivery-status.md` is separately authoritative for implementation progress and evidence; it follows the `$project-plan-execution` delivery-state contract and is not a canonical design document.

`brainstorm.md` is a chronological, non-canonical decision trail. Record meaningful milestones: the seed, newly explored directions, evidence, user feedback, alternatives, reversals, approvals, and crystallized conclusions. Update it at milestones rather than after every message.

The numbered definition documents from `01` through `08` are canonical. `experience-design.md`, when created, is an additional canonical definition document without changing the numbered contract. When thinking changes, update the relevant canonical document and record the reason in `brainstorm.md`. An abandoned idea that remains in `brainstorm.md` is not an active requirement.

The System Context is the authoritative orientation entry point, not the authoritative owner of every fact it summarizes. Current implementation evidence and approved detailed documents retain the authority described in [system-context.md](system-context.md). Keep current baseline facts out of initiative documents when they are useful across multiple initiatives, and keep proposed initiative behavior out of the current baseline until delivery verifies it.

## Change Profile ownership

For `system-change` and `hybrid` initiatives, the Change Profile defined by [change-profile.md](change-profile.md) is routing state rather than a canonical project artifact. Store its current operational value in `00-status.md`; record material transitions in `brainstorm.md`; and include concise rationale in `01-concept.md` only when it helps explain the approved design. Do not create a numbered or standalone project `change-profile.md`, list one in the artifacts map, or make it a new gate.

Use the confirmed profile to keep the artifact set proportional. Expedited work may omit technical or domain documents when the profile evidence proves they add no useful ownership. Standard and full work still create only the conditional artifacts that carry substantive content; depth is not permission to create empty placeholders.

Avoid duplicating full content across files. Link to the canonical owner of a concept and keep a consistent traceability identifier when relationships would otherwise be ambiguous, for example `REQ-`, `RULE-`, `DEC-`, and `SLICE-` identifiers. Use identifiers only when the project is complex enough to benefit from them.

## Canonical document header

Begin each numbered canonical definition document from `01` through `08`, and `experience-design.md` when present, with:

```markdown
# <Document title>

Status: Draft | Review | Approved
Last updated: YYYY-MM-DD

## Confirmed

## Assumptions

## Open decisions
```

Add only the sections needed after this shared status block. `Draft` means active definition, `Review` means presented for a gate, and `Approved` requires explicit user approval. A later material change returns the affected document to `Draft` or `Review` and may invalidate a downstream gate.

## Chat-only mode

Do not create or update files, including `00-status.md` or `system-context.md`. An existing System Context may be read as evidence. Warn that chat-only work cannot be reliably resumed from another chat. Preserve the same conceptual gates in conversation and summarize confirmed facts, assumptions, and open decisions at meaningful transitions. If the user later switches to persistent mode, ask for the target slug and crystallize the current state without inventing missing history.
