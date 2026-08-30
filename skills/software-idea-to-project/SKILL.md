---
name: software-idea-to-project
description: Start, expand, resume, or report a software definition workflow that produces approved product behavior, interaction decisions when relevant, architecture, and an implementation-ready plan. Use for software ideation, requirements, UX or interaction definition, domain modeling, technical scoping, architecture, interfaces, data, delivery planning, and cross-session handoff; do not use for dedicated visual-asset production, market validation, revenue potential, ROI, or business viability.
---

# Software Idea to Project

Turn an incomplete software idea into a coherent, traceable technical project definition. Keep decisions reversible until evidence supports committing to them, and scale the process to the idea rather than forcing every project through every artifact.

## Establish context and mode

Before asking questions or proposing a direction:

1. Locate and follow every applicable `AGENTS.md` from the workspace root to the files in scope.
2. When a repository exists, inspect only enough documentation, configuration, code, tests, and recent project evidence to ground the discussion. Preserve established conventions unless a technical reason justifies changing them.
3. Classify the request as **start**, **status**, **resume**, or **handoff**, and classify its workflow entry point as **idea**, **definition**, **experience design**, **architecture**, or **planning**.
4. For a new workflow, ask the user to choose one working mode unless their request already makes it clear:
   - **Chat-only** — develop the definition in conversation without writing artifacts.
   - **Persistent workspace** — maintain the project definition under `docs/software-design/<slug>/`. Recommend this for work expected to span multiple rounds, but require confirmation before writing.

Warn that chat-only work cannot be resumed reliably from another chat. Offer persistent mode when cross-session continuity matters, but do not create a checkpoint after the user chooses chat-only.

## Report or resume durable work

For a status, resume, or handoff request, search `docs/software-design/*/00-status.md` before asking for context or choosing a mode. Then read [references/session-state.md](references/session-state.md) and follow its discovery and recovery protocol. When a checkpoint declares `delivery_checkpoint`, read it for a combined definition-and-delivery status; delivery execution and repair belong to `$project-plan-execution`.

- If the request identifies a session, use its checkpoint.
- If exactly one relevant session exists, read it directly.
- If several plausible sessions exist, show their project, phase, phase status, last update, and next action, then ask the user to choose.
- If no checkpoint exists, say that no durable state was found. Offer to reconstruct it from existing definition artifacts or start a new persistent session; do not claim to remember another chat.

Read `00-status.md` first, then only the files listed in `required_context`. Read the complete `brainstorm.md` only for recovery, audit, or historical traceability. A status-only request is read-only and must not repair or advance the workflow.

When resuming an active session, execute the recorded `next_action` and continue autonomously rather than restarting discovery or asking for confirmation. For a waiting session, present its `pending_user_action`. Never overwrite an existing session silently.

## Enforce the boundary

This skill defines software, not its business case. Do not perform market validation, TAM or market-size analysis, pricing, monetization, customer-acquisition analysis, ROI analysis, investor analysis, business-viability analysis, or judge whether the product should exist. If requested, identify that work as outside this skill and keep it separate from the technical definition.

Questions about actors, workflows, expected volume, permissions, operating responsibility, and observable outcomes are appropriate only when their answers affect requirements or engineering decisions. Do not reinterpret them as commercial validation.

This is also a definition workflow, not implementation authorization. Until the user explicitly asks to build, implement, scaffold, or modify code:

- do not create application source, project scaffolds, migrations, infrastructure, or tests;
- do not install dependencies, provision services, or mutate external systems;
- do not turn diagrams, schemas, interface sketches, or pseudocode into production code.

Definition artifacts are allowed only after the user chooses persistent workspace or otherwise explicitly requests them.

Defining interaction behavior and the experience needed to approve the product is in scope. Producing polished visual assets, high-fidelity mockups, or interactive prototypes is not implied by this workflow; use a suitable specialized capability only when the user requests those deliverables or they are necessary evidence. Its output informs this workflow but does not approve a gate or become canonical until it is reconciled with the definition.

## Run the workflow progressively

For an early or incomplete idea, read [references/discovery.md](references/discovery.md) and move through:

`Frame → Expand → Explore → Research when needed → Refine → Crystallize`

Work on one related decision cluster at a time and complete multiple coherent, safe steps in the same turn. Inspect available evidence before asking. Ask only when the missing answer cannot be discovered and a wrong assumption would materially change scope, architecture, risk, cost, or irreversible work. Otherwise proceed with a reversible, clearly labeled assumption. Compare a small number of credible alternatives only when the choice has meaningful technical consequences.

While `phase_status` is `active`, execute `next_action` without user confirmation and keep advancing through subsequent safe actions. Updating the checkpoint or assigning a new `next_action` is bookkeeping, not a terminal condition. Stop only for genuine user input, Gate 1 or Gate 2 approval, a blocker or required authorization that cannot be resolved in scope, or completion.

Use these uncertainty labels whenever ambiguity affects the result:

- **Confirmed** — supplied by the user or established by repository evidence.
- **Assumption** — a reversible default used to maintain progress.
- **Open decision** — a choice that materially affects scope, architecture, risk, or irreversible work.

Classify the product's human interaction surface as **significant**, **minimal**, or **not applicable**. Read [references/experience-design.md](references/experience-design.md) when human interaction affects workflows, acceptance behavior, accessibility, navigation, responsive behavior, or other consequential decisions. Do not create experience artifacts for a justified not-applicable classification.

When the concept, scope, essential behaviors, domain boundaries, and applicable experience decisions are coherent, apply **Gate 1 — Design approval**. Present the proposed design and its remaining open decisions. For a significant or minimal interaction surface, include the applicable experience-readiness result; for a not-applicable surface, state the reason briefly. Do not begin detailed architecture until the user explicitly approves it in chat or approves the relevant persistent documents.

After Gate 1, read [references/technical-design.md](references/technical-design.md). Define only the architecture, data, interfaces, decisions, and operational qualities the project actually needs. Move backward if this work exposes a contradiction in the approved design.

Then apply **Gate 2 — Architecture readiness**. Confirm that implementation-blocking choices are resolved, requirements trace to technical decisions, interfaces and ownership are coherent, risks have a treatment, and the validation approach is known. Do not create an implementation plan while blockers remain.

After Gate 2, read [references/implementation-planning.md](references/implementation-planning.md) and produce an adaptive, executable plan. Precision must come from repository evidence or approved greenfield structure, never invention.

## Maintain artifacts deliberately

In persistent mode, read [references/artifacts.md](references/artifacts.md) and [references/session-state.md](references/session-state.md) before creating or updating files. Create `00-status.md` and `brainstorm.md` when the session begins. Maintain the checkpoint after meaningful transitions and create canonical definition documents only when their content is useful. Do not create empty placeholders or all documents by default.

Keep traceability from the original need to requirements, applicable experience decisions, domain rules, technical decisions, interfaces, and implementation slices. Mark each canonical document `Draft`, `Review`, or `Approved`, and distinguish confirmed facts, assumptions, and open decisions.

## Finish at the correct boundary

Lead each response with the most useful current result. Prefer reaching a gate, a genuine blocker, or another meaningful phase boundary before yielding. Do not end merely because one decision was recorded or a new `next_action` was selected.

When user input genuinely blocks progress, ask the smallest question that resolves it. When ending at a natural boundary with `phase_status: active`, report the saved `next_action` as informational status, not as a question or request for permission.

In persistent mode, update the durable checkpoint before deliberately ending, requesting blocking input, requesting gate approval, reporting a new blocker, or handing work to another agent.

Completing the implementation plan does not authorize implementation. If the user explicitly authorizes implementation, require a concrete authorized slice list and hand the approved requirements, assumptions, deferred decisions, plan, and applicable repository instructions to `$project-plan-execution`. Keep this definition workflow complete; do not implement from this skill.
