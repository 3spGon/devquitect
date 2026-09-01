# System Context and Baseline

Read this reference when `docs/software-design/system-context.md` exists, when persistent work needs to establish it, or when repository evidence suggests that its relevant coverage is stale.

## Purpose and location

`system-context.md` is the shared, tool-neutral orientation document for the maintained system. It describes the current baseline at the depth needed to ground later initiatives without rediscovering the whole repository. Store it by default at:

```text
docs/software-design/system-context.md
```

This first version assumes one primary system per repository. Do not introduce a multi-system directory scheme without a demonstrated need.

The System Context belongs to the system, not to one definition session. It is not a numbered initiative artifact, is not listed in a session's `artifacts` map, and is not approved by Gate 1 or Gate 2. A session may point to it through the optional `system_context` checkpoint field.

## Document contract

Start the document with:

```yaml
---
schema_version: 1
document: system-context
system: <name>
scope: repository
lifecycle: proposed
context_status: partial
revision: 1
last_updated: YYYY-MM-DD
baseline_reference: null
---
```

Use these values:

- `lifecycle`: `proposed`, `in-development`, `operational`, or `retired`.
- `context_status`: `partial`, `current`, or `stale`.
- `revision`: a positive integer incremented once per coherent update.
- `last_updated`: the date of the latest coherent update.
- `baseline_reference`: the commit, branch, release, environment, or other explicit reference represented by the document; use `null` when no implemented baseline exists or no reliable reference is available.

`partial` means the document is useful but has declared gaps. `current` means it is sufficiently verified for its stated scope and baseline, not that it exhaustively documents the repository. `stale` means known material changes or contradictory evidence require a refresh.

## Content

Begin with a short **Quick orientation**. Add only the sections that contain useful information:

- **Purpose** — the technical problem or workflow the system supports.
- **Current lifecycle** — what the lifecycle value means for this system now.
- **System boundaries** — what is inside and outside the system.
- **Actors and external systems** — relevant users, operators, and integrations.
- **Current capabilities** — behavior available in the represented baseline.
- **Core workflows** — the few workflows needed to understand later changes.
- **Technical landscape** — major components, runtimes, and structural relationships.
- **Data and ownership** — important sources of truth and ownership boundaries.
- **Integrations** — consequential external dependencies and contracts.
- **Engineering constraints** — compatibility, security, performance, deployment, or operational constraints.
- **Development and verification** — confirmed commands and procedures for running and validating the system.
- **Preserved behavior** — invariants or behavior future initiatives must protect.
- **Known limitations and context gaps** — limitations and unverified areas that affect confidence.
- **Authoritative references** — links to detailed documentation, decisions, contracts, or repository locations.

Do not create empty sections. Keep the document suitable for quick orientation: summarize and link instead of duplicating READMEs, architecture documents, contracts, or inventories. Do not record installed skills, analysis tools, generated reports, or tool-specific metadata.

## Establish the baseline proportionally

For a **new-system** initiative, create the document only after confirmed information can make it useful. Start with `lifecycle: proposed`, `context_status: partial`, and `baseline_reference: null`; evolve it as approved definition and verified implementation establish the baseline.

For a **system-change** initiative, read an existing context first. If it is current and sufficient for the affected area, reuse it without rewriting it. If it is missing, stale, or insufficient, inspect repository evidence and establish or refresh only the affected sections needed to analyze the requested delta safely. Do not block a localized change on documenting unrelated parts of the system.

For a **hybrid** initiative, distinguish the new component's proposed state from the existing system baseline and the integration constraints between them.

In chat-only mode, use an existing document as evidence but never create or update it. In persistent mode, do not create an empty placeholder: wait until the document can provide meaningful orientation.

## Authority and current versus proposed state

Use source authority deliberately:

- Code, configuration, migrations, and tests establish the implemented baseline.
- Approved definition documents establish desired behavior and design.
- Decision records explain rationale.
- The System Context summarizes and links; it does not override these detailed sources.

Never describe planned behavior as currently implemented. During planning, add a context refresh to the delivery slice that will materially change the baseline; update the document only after that behavior is implemented and verified. A greenfield document may describe a proposed system only while its `lifecycle` and `baseline_reference` make that status explicit.

When evidence contradicts the document, determine whether the context is stale, the implementation diverges from approved design, or baselines differ. Do not silently choose one. Correct or mark stale only in persistent work. A context correction does not automatically invalidate a gate, but a discovered false premise invalidates every gate that depends materially on it.

## Update discipline

Update the System Context only when purpose, boundaries, implemented capabilities, major structure, data ownership, integrations, engineering constraints, verification procedures, preserved behavior, lifecycle, or known gaps change materially.

Before writing, remember the current `revision`, re-read the document, and stop to reconcile if another writer changed it. Apply one coherent update, increment `revision` once, refresh `last_updated` and `baseline_reference` as evidence allows, and keep unrelated content intact.
