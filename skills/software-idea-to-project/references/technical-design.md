# Technical Design

Read this reference only after Gate 1 has been approved, or when the user supplies an already approved definition. Produce the minimum technical design needed to make implementation safe and predictable.

## Derive the architecture

Anchor every structural choice in an approved requirement, repository constraint, or operational need. Reuse an existing stack and its established boundaries when appropriate. Do not propose unrelated modernization or replacement.

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

Connect each major requirement to the component, domain rule, interface, or decision that satisfies it. Surface requirements with no technical treatment and technical components with no approved purpose.

If architecture work contradicts the approved design, return to discovery, update the affected canonical documents, and repeat Gate 1 for the material change.

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

Present the readiness summary and request explicit approval. In persistent mode, move relevant technical documents to `Review`, then `Approved` after user approval. Do not create `08-implementation-plan.md` until this gate passes.
