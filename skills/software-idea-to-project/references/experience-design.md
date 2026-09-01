# Experience Design

Read this reference before Gate 1 when human interaction materially affects workflows, acceptance behavior, accessibility, navigation, responsive behavior, or another consequential product decision. Define only the experience needed to make the software behavior coherent and implementation-ready; do not require visual deliverables by default.

## Classify the interaction surface

Classify the project using repository and user evidence:

- **Significant** — users complete multi-step, stateful, safety-sensitive, permission-sensitive, or cross-device workflows whose interaction choices affect requirements or architecture.
- **Minimal** — the interface is narrow, but a small number of interaction states or accessibility expectations affect acceptance.
- **Not applicable** — no human-facing interaction needs definition, such as a backend service, worker, library, or machine-only integration. Record the reason in the Gate 1 summary; do not create an experience artifact solely to hold that classification.

Reclassify when later evidence changes the product boundary. Scale the depth to the consequences of a wrong decision rather than to the number of screens.

For `system-change` and `hybrid` initiatives, record `experience` as an affected Change Profile surface when observable interaction behavior changes. A significant experience change disqualifies expedited routing. A minimal change may remain expedited only when all interaction states, acceptance behavior, accessibility effects, and recovery behavior are known and no other disqualifier in [change-profile.md](change-profile.md) applies.

## Define the consequential experience

For significant or minimal surfaces, define only what applies:

- user tasks, entry points, primary and alternate flows, and observable completion;
- information architecture, navigation, orientation, and return paths;
- views or interaction surfaces and the responsibilities of important reusable components;
- loading, empty, partial, error, success, unavailable, permission-denied, interrupted, and recovery states;
- responsive behavior, supported input methods, platform conventions, and continuity across devices where relevant;
- accessibility requirements such as keyboard operation, focus order, semantics, contrast constraints, reduced motion, text scaling, and announcements where they affect acceptance;
- content or feedback needed for users to understand state, consequences, destructive actions, and recovery;
- existing design-system components, tokens, content conventions, and repository constraints that should be reused.

Prefer behavioral descriptions and testable outcomes over styling detail. Do not invent a new visual language when an established design system exists. Record any necessary deviation as a consequential decision with its rationale and compatibility cost.

For a consequential interaction choice, compare a small number of credible alternatives. Record the selected option, the user or system need it serves, rejected alternatives, consequences, and the evidence or condition that would justify revisiting it.

## Use specialized design capabilities conditionally

Use an available UX, product-design, prototyping, or visual-production capability only when the user requests its deliverables or when visual evidence is necessary to resolve a material decision. Provide it the approved or current concept, requirements, actors, constraints, target platforms, and known design system.

Treat its result as evidence. Reconcile these outputs into the definition:

- flows and information architecture;
- view, component, and state inventories;
- alternatives and recommended decisions with rationale;
- remaining open decisions;
- links or references to produced mockups or prototypes.

`software-idea-to-project` remains responsible for canonical artifacts, uncertainty labels, traceability, and Gate 1 approval. A mockup, prototype, external review, or specialized-skill result is never approval by itself.

## Persist only when useful

In persistent mode, create `experience-design.md` only when the experience definition is substantive enough to need a canonical owner. Use the canonical document header from [artifacts.md](artifacts.md), list it in the checkpoint only after creation, and include it in `required_context` only when the active action or pending approval depends on it.

Keep requirement statements in `02-requirements.md` and cross-cutting rationale in `07-decisions.md` when those are their canonical owners. Link rather than duplicate them from `experience-design.md`. For a minimal surface, those existing documents may be sufficient; do not create the optional artifact merely for symmetry.

## Apply experience readiness at Gate 1

The experience portion of Gate 1 is ready when, at the depth the project needs:

- primary tasks and alternate or recovery flows are coherent;
- consequential views, states, navigation, and system feedback are defined;
- responsive, input-method, platform, and accessibility behavior that affects acceptance is known;
- design-system reuse or justified deviation is explicit;
- experience decisions trace to requirements and acceptance behavior;
- implementation-blocking interaction choices are resolved;
- confirmed facts, assumptions, and non-blocking open decisions are visible.

Wireframes and prototypes are evidence, not universal gate requirements. Move applicable experience documents to `Review` before requesting Gate 1 approval and to `Approved` only after explicit user approval. A later material change to an approved flow, navigation model, state behavior, accessibility contract, or design-system decision invalidates Gate 1 and therefore Gate 2.

When later experience evidence widens impact or reveals an expedited disqualifier, elevate the Change Profile visibly and apply its gate invalidation rules. Do not keep expedited depth merely because the implementation surface is visually small.
