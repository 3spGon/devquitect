# Proportional Change Profile decisions

Status: Approved
Last updated: 2026-08-31

## Confirmed

- Gate 1 and Gate 2 were explicitly approved in chat on 2026-08-31.

## Assumptions

- The repository's English documentation convention remains appropriate for maintainability.

## Open decisions

No implementation-blocking decisions remain.

## DEC-001 — Use a routing profile, not a generated artifact

**Decision:** Store operational state in `00-status.md`, allow concise rationale in `01-concept.md`, and create no project `change-profile.md`.

**Rationale:** The profile controls workflow depth and changes as evidence develops. A separate canonical artifact would duplicate state and encourage unnecessary ceremony.

**Rejected:** Always generate a dedicated profile document; infer depth without recording it.

## DEC-002 — Default provisional work to standard

**Decision:** Use standard as the fail-safe provisional depth.

**Rationale:** Expedited requires positive evidence; full requires known material risk. Standard preserves progress without prematurely claiming either condition.

## DEC-003 — Permit combined approval only for confirmed expedited work

**Decision:** One explicit approval may cover Gate 1 and Gate 2 only when a bounded assessment proves no material architecture change is needed.

**Rationale:** Repeating two approval prompts with identical evidence adds no safety. The combined action preserves both authorization boundaries while remaining proportional.

**Rejected:** Remove Gate 2 for small changes; self-approve Gate 2; perform detailed architecture before Gate 1.

## DEC-004 — Retain checkpoint schema version 2

**Decision:** Add `change_profile` as an optional nested field without a version bump.

**Rationale:** The extension is backward-compatible and has an unambiguous absent-state interpretation. Mandatory migration would add risk without benefit.

## DEC-005 — Centralize normative rules

**Decision:** Make `references/change-profile.md` authoritative and keep integration references narrow.

**Rationale:** Depth and invalidation rules are safety-sensitive. Duplication would make contradictions likely.

## DEC-006 — Elevate automatically and visibly

**Decision:** New risk evidence increases depth without asking permission to perform additional analysis, but the response shows the evidence, transition, and gate consequences.

**Rationale:** Safety should not depend on user awareness of workflow mechanics, while authorization changes must remain transparent.

## DEC-007 — Preserve downstream skill contracts

**Decision:** Do not modify `project-plan-execution` or `targeted-refactoring`.

**Rationale:** Execution already consumes final gate and plan state. Refactoring already owns behavior-preserving structural work. Direct coupling would weaken composition.

## DEC-008 — Treat the behavioral change as a compatible feature addition

**Decision:** Preserve existing sessions and sequential workflows while adding proportional routing and focused cases.

**Rationale:** Existing valid inputs and safety guarantees remain supported. Release classification is expected to be minor, but release and promotion remain outside this initiative unless separately authorized.
