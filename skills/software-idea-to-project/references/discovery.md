# Discovery and Crystallization

Read this reference when the input is an early idea, incomplete definition, conflicting requirements, or a request to clarify what the software should do. Stop using it once Gate 1 is approved unless later work exposes a contradiction.

## Frame

Establish the smallest useful shared understanding:

- the technical problem or workflow being supported;
- actors and external systems that interact with it;
- the primary observable outcome;
- hard constraints already supplied by the user or repository;
- the boundary between this system and its environment.

Distinguish an actor who determines system behavior from a buyer or market segment. The former is in scope; commercial evaluation is not.

If the request contains multiple independently deployable subsystems, surface that early. Identify their relationships and choose one coherent boundary to define first rather than refining an unbounded platform all at once.

## Expand

Explore only dimensions that can change requirements or architecture:

- primary and alternate workflows;
- inputs, outputs, triggers, and observable completion;
- important scenarios and failure paths;
- business-domain rules expressed as system behavior;
- permissions, trust, ownership, and data sensitivity;
- scale, latency, availability, retention, accessibility, and compliance constraints when relevant;
- explicit first-release scope, later possibilities, and non-goals.

Prefer concrete scenarios over feature lists. For each important workflow, identify the initiating event, relevant state, decisions, side effects, failure behavior, and final observable result.

## Explore technical alternatives

Use several technical lenses where helpful:

- **Behavior lens** — what users and external systems can observe.
- **Domain lens** — concepts, identities, rules, lifecycle, and invariants.
- **System lens** — boundaries, dependencies, integration patterns, and failure isolation.
- **Operational lens** — security, privacy, reliability, performance, observability, and support responsibility.
- **Delivery lens** — smallest vertical slice, validation cost, reversibility, and migration risk.

When a decision is consequential, present two or three credible options with the constraints each optimizes, their costs, and a recommendation. Do not generate alternatives merely to satisfy a quota.

## Research only when it changes a decision

Research external sources when current facts, standards, vendor capabilities, library behavior, protocol rules, or existing technical patterns could materially change the definition. Prefer primary and authoritative sources, cite them near the supported claim, and distinguish sourced facts from inference.

Do not research market demand, competitors for commercial positioning, pricing opportunity, TAM, ROI, or whether the product should be built. Technical build-versus-integrate analysis is allowed only as an engineering boundary decision, not as a business-viability judgment.

## Refine

Challenge the emerging definition for:

- contradictory scenarios or requirements;
- missing ownership or ambiguous identity;
- invalid state transitions and concurrency conflicts;
- retry, duplication, ordering, replacement, cancellation, and partial-failure behavior;
- unclear responsibility between the system and its integrations;
- speculative features that entered scope without supporting need;
- irreversible choices based only on assumptions.

Resolve material contradictions with the user. Record reversible gaps as assumptions and consequential unresolved choices as open decisions.

## Crystallize and apply Gate 1

The design is ready for review when it contains, at the depth the project needs:

- purpose, actors, system boundary, and primary workflows;
- first-release scope, non-goals, and testable acceptance behavior;
- domain concepts, important rules, ownership, and major failure behavior;
- constraints and non-functional requirements that affect the design;
- confirmed facts, assumptions, and open decisions;
- a recommended technical direction at a conceptual level, without premature file-level planning.

Present a concise design summary and any open decisions. Ask for explicit approval. In persistent mode, update the applicable concept, requirements, and domain documents to `Review`; mark them `Approved` only after the user approves. Detailed architecture begins only after this gate passes.
