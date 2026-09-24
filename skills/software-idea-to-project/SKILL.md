---
name: software-idea-to-project
description: Start, expand, resume, or report a software definition workflow for a new system, a change to an existing system, or a hybrid initiative, producing approved product behavior, interaction decisions when relevant, architecture, and an implementation-ready plan. Use for software ideation, requirements, UX or interaction definition, domain modeling, technical scoping, architecture, interfaces, data, delivery planning, and cross-session handoff; do not use for dedicated visual-asset production, market validation, revenue potential, ROI, or business viability.
---

# Software Idea to Project

Turn an incomplete software idea or change request into a coherent, traceable technical definition. Keep the workflow proportional to the initiative and decisions reversible until evidence supports them.

## Scope and authority

This skill defines the software and its engineering plan, not its business case. Do not perform market, commercial, ROI, or business-viability analysis. Treat questions about users, workflows, volume, permissions, and operating responsibility as engineering inputs only when they change requirements or technical decisions.

Definition is not implementation authorization. Do not create or modify application code, tests, migrations, infrastructure, or dependencies; install packages; provision services; or mutate external systems from definition work. A completed plan authorizes nothing by itself; implementation must use `$project-plan-execution` with an explicit slice list.

Interaction behavior that affects approval, accessibility, or workflows belongs here. Polished visuals and prototypes require a separate request or a clear need as evidence; generated assets do not approve gates or become canonical until reconciled with the definition.

## Route the definition workflow

Follow applicable `AGENTS.md` instructions and inspect only the repository evidence needed to establish context. Classify a request as start, status, resume, or handoff; identify whether it concerns a new system, a system change, or both; then use the reference that owns the current phase:

- For early or incomplete ideas, follow [discovery.md](references/discovery.md). Both design gates require explicit approval.
- For system changes, use [change-profile.md](references/change-profile.md) to select proportional workflow depth. Use [experience-design.md](references/experience-design.md) when interaction decisions affect acceptance or usability.
- After Gate 1, use [technical-design.md](references/technical-design.md) for architecture readiness. After Gate 2, use [implementation-planning.md](references/implementation-planning.md) to produce an evidence-based plan.
- For persistent sessions, use [artifacts.md](references/artifacts.md), [session-state.md](references/session-state.md), and [system-context.md](references/system-context.md) for artifact ownership, state transitions, and the shared baseline.

Ask for a working mode only when the request leaves it unclear. Chat-only work creates no durable files; persistent sessions live under `docs/software-design/<slug>/` and require the user's choice or explicit request. Do not create placeholders or documents without useful content.

For status, resume, or handoff, start with `00-status.md` and follow [session-state.md](references/session-state.md). A declared `delivery_checkpoint` combines definition and delivery status; execution and repair remain with `$project-plan-execution`. Status-only requests are read-only. On active sessions, follow the saved `next_action`; preserve existing sessions and user changes.

## Finish at the definition boundary

Maintain traceability from the need through requirements, experience decisions, domain rules, technical choices, interfaces, and slices. Mark canonical documents `Draft`, `Review`, or `Approved`, and keep confirmed facts, assumptions, and open decisions distinct. Update persistent state at meaningful transitions and before handing off or yielding at a gate or blocker.

Once the plan is ready, hand its approved requirements, assumptions, deferred decisions, and repository instructions to `$project-plan-execution` only after the user explicitly authorizes concrete slices. Keep the definition phase complete and do not implement from this skill.
