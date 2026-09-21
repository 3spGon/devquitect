# Evaluation Authentication Governance decisions

Status: Approved
Last updated: 2026-09-21

## Confirmed

- Gate 1 was explicitly approved by the user on 2026-09-21.
- The initiative must not make a personal ChatGPT subscription an implicit dependency of an
  evaluation command.

## Assumptions

- The choices below are the recommended technical direction pending Gate 2 approval and external
  policy confirmation.

## Open decisions

None.

## DEC-EAG-001 — Retain local subscription mode only as explicit opt-in

**Decision:** Keep a narrowly scoped `chatgpt-cache-local` mode as a possible operator-run diagnostic,
but remove implicit discovery and prohibit it from unattended execution until policy approval.

**Rationale:** Immediate removal would be safer but needlessly breaks a potentially useful local
diagnostic path. Keeping it explicit preserves reversibility without normalizing subscription loops.

**Rejected:** Keep automatic discovery; it hides a sensitive side effect. Remove all support now;
revisit if policy confirms that no supported local diagnostic use exists.

## DEC-EAG-002 — Use one explicit auth-mode boundary

**Decision:** Expose one small `--auth-mode` contract plus mode-specific validation rather than a
provider plugin framework.

**Rationale:** The current system has only credential-free, API/business, and local-cache needs.
The smallest boundary that makes policy visible is easier to audit and test.

**Rejected:** A generic provider registry; it would add scaffolding before a second provider requires it.

## DEC-EAG-003 — Best-effort stale cleanup with no SIGKILL claim

**Decision:** Use one cleanup scope for staging and execution, create restrictive files atomically,
and add conservative startup scavenging for marked, old, non-live attempt roots.

**Rationale:** Python cannot guarantee `finally` after forcible parent termination. A marker/age/
liveness policy reduces residual risk without pretending to provide an impossible guarantee.

**Rejected:** Claim immediate deletion under all crashes; unsupported. An external supervisor remains
a future option if unattended execution requires stronger guarantees.

## DEC-EAG-004 — Prohibit unattended subscription-cache execution

**Decision:** `chatgpt-cache-local` is permitted only for an explicitly launched, local, supervised
run. It is prohibited in CI, cron, schedulers, daemons, automatic retries, recurring loops, and
promotion or publication workflows.

**Rationale:** This is the narrowest boundary that matches the current operating model. It avoids
claiming that temporary-file hygiene authorizes automated use of a subscription, while preserving a
human-reviewed diagnostic path. A future change requires a new policy review and gate invalidation.

**Status:** Approved by the user with Gate 2 on 2026-09-21.
