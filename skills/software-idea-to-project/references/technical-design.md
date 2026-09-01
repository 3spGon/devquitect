# Technical Design

Read this reference after Gate 1 has been approved, when the user supplies an already approved definition, or only for the bounded expedited assessment described below. Produce the minimum technical design needed to make implementation safe and predictable.

## Assess an expedited no-change path

Before combined Gate 1 and Gate 2 approval, a confirmed expedited initiative may assess whether the current architecture can absorb the delta without material change. Limit this assessment to existing component ownership, data and state, interfaces, trust boundaries, operational behavior, compatibility, acceptance, verification, and rollback. Do not create detailed proposed architecture or begin ordinary technical design before Gate 1.

If any material architecture treatment, migration, trust-boundary change, incompatible contract, consequential integration, or complex operational behavior is needed, the initiative is not expedited. Elevate it according to [change-profile.md](change-profile.md) and return to the sequential Gate 1 flow.

## Derive the architecture

Anchor every structural choice in an approved requirement, repository constraint, or operational need. Reuse an existing stack and its established boundaries when appropriate. Do not propose unrelated modernization or replacement.

For system-change and hybrid initiatives, separate **current architecture** established by the System Context and repository evidence from **proposed architecture** owned by the initiative documents. Identify unchanged components, changed components, new boundaries, compatibility constraints, migration needs, and preserved behavior. Never rewrite the current baseline to make the proposal appear implemented.

Define as relevant:

- components and their single responsibilities;
- synchronous calls, asynchronous events, and data flow;
- source of truth and ownership for each important concept;
- trust boundaries, authentication, authorization, and sensitive-data handling;
- failure isolation, retries, idempotency, ordering, and consistency expectations;
- deployment, scaling, observability, backup, recovery, migration, and compatibility concerns.

Compare alternatives for consequential decisions. Record the chosen option, its technical rationale, rejected alternatives, consequences, and conditions that would justify revisiting it.

## Model the domain and data

Define only entities and relationships that serve approved behavior. For each important concept, capture identity, ownership, lifecycle, state transitions, invariants, validation, retention, and deletion behavior.

Separate domain concepts from storage representation. Add a data model when persistence, relationships, querying, lifecycle, or migration complexity warrants it. Address concurrency and uniqueness where competing operations can violate an invariant.

## Define interfaces and contracts

Specify contracts at system or component boundaries when another implementer or system must depend on them:

- operation, command, event, or endpoint purpose;
- caller and owner;
- input and output shapes at the necessary level of precision;
- validation, authorization, idempotency, errors, and retry semantics;
- ordering, versioning, compatibility, and deprecation where relevant;
- webhooks or events, including trigger, payload responsibility, delivery expectations, and duplicate handling.

Do not invent endpoint paths, field names, or protocol details before the architecture supports them. In an existing codebase, align contracts with current conventions.

## Preserve traceability

Connect each major requirement and approved experience decision to the component, domain rule, interface, or decision that satisfies it. Surface requirements or interaction constraints with no technical treatment and technical components with no approved purpose.

If architecture work contradicts the approved design or requires a material change to an approved experience decision, return to discovery, update the affected canonical documents, and repeat Gate 1 for the material change.

If repository evidence contradicts the System Context, reconcile or mark the context stale in persistent mode. A context correction alone does not invalidate a gate; invalidate affected gates only when the contradiction exposes a false material premise in the approved design or architecture.

For system-change and hybrid work, update the Change Profile when technical evidence changes impact or affected surfaces. A purely technical contradiction after approval preserves Gate 1 and invalidates Gate 2; a contradiction that changes approved behavior returns to the earliest affected design phase.

## Apply Gate 2 — Architecture readiness

Architecture is ready for planning only when:

- every implementation-blocking choice is resolved;
- component responsibilities and ownership do not overlap ambiguously;
- important data lifecycle and state transitions are defined;
- external and internal contracts are coherent enough to implement;
- security, privacy, reliability, performance, and compliance risks have an explicit treatment when applicable;
- migrations, rollout, rollback, and compatibility needs are known where applicable;
- acceptance and validation strategy are known;
- confirmed facts, assumptions, non-blocking deferred decisions, and risks are explicit;
- requirements trace to technical design elements.
- approved experience decisions trace to technical design elements when applicable.

Present the readiness summary and request explicit approval. In persistent mode, move relevant technical documents to `Review`, then `Approved` after user approval. Do not create `08-implementation-plan.md` until this gate passes.

For a confirmed expedited initiative, the bounded no-change assessment satisfies the architecture-readiness portion only through the explicit combined approval contract in [change-profile.md](change-profile.md). It never self-approves Gate 2 and never authorizes implementation.
