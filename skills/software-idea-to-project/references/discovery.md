# Discovery and Crystallization

Read this reference when the input is an early idea, incomplete definition, conflicting requirements, or a request to clarify what the software should do. Stop using it once Gate 1 is approved unless later work exposes a contradiction.

## Establish initiative context and baseline

Classify the initiative before framing it:

- **new-system** — the initiative defines a new maintained system;
- **system-change** — the initiative changes an implemented system;
- **hybrid** — it introduces a new component or boundary that must integrate with an implemented system.

For system-change and hybrid work, read the System Context when present and establish a sufficiently verified baseline for the affected area before defining the requested delta. If the context is missing or stale, inspect only the relevant documentation, code, configuration, tests, and recent evidence. In persistent mode, create or refresh `docs/software-design/system-context.md` according to [system-context.md](system-context.md); in chat-only mode, keep the reconstructed baseline in conversation and do not write it.

After enough evidence exists to state the affected baseline and requested delta, read [change-profile.md](change-profile.md). Initialize the applicable Change Profile as provisional and standard, then refine it as discovery establishes change kinds, impact, affected surfaces, preserved behavior, risk, and verification. Do not confirm expedited routing merely because the requested edit appears small.

For new-system work, do not create an empty System Context. In persistent mode, create it only after the emerging definition contains useful confirmed purpose, boundary, lifecycle, or constraints. Keep proposed facts visibly distinct from an implemented baseline.

## Frame

Establish the smallest useful shared understanding:

- the technical problem or workflow being supported;
- actors and external systems that interact with it;
- the primary observable outcome;
- hard constraints already supplied by the user or repository;
- the boundary between this system and its environment.

For system-change and hybrid initiatives, state the observable current behavior, the requested delta, and the behavior that must remain unchanged. Do not treat a feature list as a sufficient baseline or acceptance definition.

Distinguish an actor who determines system behavior from a buyer or market segment. The former is in scope; commercial evaluation is not.

If the request contains multiple independently deployable subsystems, surface that early. Identify their relationships and choose one coherent boundary to define first rather than refining an unbounded platform all at once.

## Expand

Explore only dimensions that can change requirements or architecture:

- primary and alternate workflows;
- human interaction surfaces, navigation, feedback, and accessibility expectations when they affect observable behavior;
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
- the interaction-surface classification and, when applicable, the experience-readiness criteria from [experience-design.md](experience-design.md);
- confirmed facts, assumptions, and open decisions;
- a recommended technical direction at a conceptual level, without premature file-level planning.

For system-change and hybrid initiatives, also confirm the Change Profile when evidence is sufficient. Present its depth and rationale with the design review. Keep it provisional and use standard depth when uncertainty is non-blocking; use full when confirmed risk requires it.

Present a concise design summary and any open decisions. Ask for explicit approval. In persistent mode, update the applicable concept, requirements, domain, and experience documents to `Review`; mark them `Approved` only after the user approves. Detailed architecture begins only after this gate passes.

Standard and full profiles use the ordinary Gate 1 transition. A confirmed expedited profile follows the combined approval contract in [change-profile.md](change-profile.md); if its no-change architecture assessment fails, elevate it and return to the ordinary Gate 1 flow.
