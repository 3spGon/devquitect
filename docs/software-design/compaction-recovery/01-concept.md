# Compaction Recovery concept

Status: Approved
Last updated: 2026-09-19

## Confirmed

- This initiative changes the existing Devquitect plugin and `project-plan-execution` workflow.
- `09-delivery-status.md` is the current durable execution checkpoint and already owns the active slice, next action, required context, blockers, and verification evidence.
- Existing resume behavior requires checkpoint re-read, plan validation, inspection of in-progress work, and conservative recovery when checkpoint and repository evidence disagree.
- Current Devquitect packages contain the plugin manifest and skill files, but not plugin hooks.
- Current official Codex behavior provides a synchronous `SessionStart` hook with `source: "compact"` before the next model request, including automatic mid-turn compactation. It can inject concise developer context. See [OpenAI Codex hooks documentation](https://developers.openai.com/codex/hooks/).
- Current official Codex behavior does not make `PreToolUse` a complete control boundary: hosted tools are not covered and specialized tool paths may bypass it.

## Assumptions

None. Unknown schema and packaging details are open technical decisions, not accepted requirements.

## Open decisions

- `DEC-CR-002`: choose the compatible checkpoint schema-evolution mechanism during technical design; existing checkpoints must remain readable and cannot be silently treated as having execution-frontier evidence they do not contain.

## Problem

Long authorized delivery runs can compact their conversational history several times. The current durable state is sufficient for an intentional resume or handoff, but compactation is not an explicit recovery boundary and the checkpoint may be too coarse or stale to reconstruct the exact work frontier. Continuing from the compacted conversation can repeat completed work, skip partial work, or trust stale memory over repository evidence.

## Desired outcome

After every root-session compactation during an active authorized delivery, Codex receives a small recovery directive before its next model request, rehydrates the authoritative delivery checkpoint, reconciles it with repository reality, loads only the current slice's required context, and continues the recorded frontier without unjustified repetition or advancement.

## System boundary

Inside this initiative:

- the `project-plan-execution` delivery-state and execution contracts;
- the execution frontier and milestone update cadence in `09-delivery-status.md`;
- a Devquitect plugin lifecycle hook for the Codex compactation boundary;
- plugin validation, packaging, and compatibility rules needed to ship that hook;
- deterministic tests and authorized behavioral evaluations for recovery behavior.

Outside this initiative:

- reducing compactation frequency;
- general-purpose memory or embeddings;
- Context Mode integration;
- exhaustive tool-log persistence;
- a second durable task-state store;
- concurrent multi-agent state coordination.

## Actors and external systems

- **Codex runtime** emits the supported compactation/session lifecycle event and injects hook output before the next model request.
- **Devquitect recovery hook** recognizes only the supported compactation entry point and emits bounded recovery context.
- **Project Plan Execution** interprets the delivery checkpoint and performs conservative recovery.
- **Repository** provides the observable implementation and verification reality against which checkpoint claims are checked.
- **Operator** reviews/trusts the plugin hook and resolves genuinely ambiguous session selection or repository contradictions.

## Primary workflow

1. Authorized slice work reaches a meaningful progress milestone and refreshes the existing delivery checkpoint.
2. Codex compacts the root session.
3. The packaged synchronous `SessionStart(source="compact")` hook runs before the next model request.
4. If no active Devquitect delivery is present, the hook is silent. Otherwise it injects a concise recovery directive and candidate checkpoint path or paths.
5. Codex treats the event as a resume: it re-reads the selected checkpoint and approved plan state, inspects relevant repository changes and evidence, and reads only `required_context`.
6. If evidence agrees, Codex resumes the recorded in-progress or next action. If evidence disagrees or session selection is ambiguous, it stops normal implementation and exposes the minimum discrepancy or choice needed.

## Conceptual direction

Use the runtime's native pre-model compactation continuation hook rather than creating an ephemeral marker and waiting for a later tool call. Keep enforcement layered:

```text
SessionStart(source="compact") recovery directive
            +
project-plan-execution recovery contract
            +
09-delivery-status.md execution frontier
            +
repository and verification evidence
```

`09-delivery-status.md` remains the only durable execution state. Hook output is a transient recovery trigger, not authority.

## Change Profile

- Status: Confirmed
- Kinds: behavior change, new capability, technical change
- Impact: Cross-cutting
- Depth: Full
- Affected surfaces: behavior, minimal experience, interfaces, operations, quality attributes, migration compatibility
- Elevation reasons: runtime hook integration, package-contract expansion, delivery-checkpoint compatibility, and multi-layer recovery evaluation

## Interaction surface

Minimal. There is no new application UI. The consequential states are hook trust accepted, hook unavailable/disabled, no active delivery, one active delivery, multiple candidate deliveries, successful recovery, and checkpoint/repository disagreement. Existing Codex hook review is reused; Devquitect must not claim automatic protection when the hook did not run.

## Gate 1 proposal

Approve the outcome, boundary, actors, workflow, non-goals, full-depth Change Profile, minimal interaction behavior, and `SessionStart(source="compact")` conceptual direction. Approval authorizes detailed architecture only; it does not authorize implementation.

Gate 1 was explicitly approved in chat on 2026-09-19.
