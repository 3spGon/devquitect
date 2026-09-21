# Evaluation Authentication Governance domain

Status: Approved
Last updated: 2026-09-21

## Confirmed

- Authentication is currently inferred from the presence of a local `auth.json`; this initiative
  changes that behavior to an explicit policy decision.
- The credential lifecycle is per evaluation attempt and must not become part of the skill snapshot,
  fixture workspace, or evidence report.

## Assumptions

- The proposed local subscription mode remains available for a human operator, but is prohibited
  from unattended execution by the approved project policy.
- No credential is persisted as domain data; the state below is operational metadata only.

## Open decisions

None.

## Concepts and ownership

| Concept | Values or states | Owner | Persistence |
| --- | --- | --- | --- |
| `AuthMode` | `credential-free`, `api-key`, `chatgpt-cache-local` | CLI policy layer | report metadata only |
| `ExecutionContext` | `structural`, `interactive-behavioral`, `unattended-behavioral` | command invocation | report metadata only |
| `AuthDecision` | `allowed`, `refused`, `missing`, `invalid` | auth policy evaluator | report metadata only |
| `CredentialState` | `not-needed`, `injected`, `staged`, `cleaned`, `stale`, `cleanup-failed` | attempt lifecycle | bounded runtime state |
| `Attempt` | `created`, `running`, `completed`, `failed`, `expired` | evaluation runner | temporary filesystem |

## Rules

1. `credential-free` is the only valid mode for the ordinary structural check.
2. `api-key` may be allowed for behavioral execution when the approved environment supplies the
   credential through the supported environment boundary.
3. `chatgpt-cache-local` requires explicit operator intent and is never valid for unattended
   execution under the approved policy.
4. An `AuthDecision` of `refused`, `missing`, or `invalid` prevents credential staging and Codex
   launch.
5. `CredentialState` can move from `staged` or `injected` to `cleaned` only after the attempt's
   parent process performs the cleanup action. A forced parent termination may leave `stale` state;
   the system must not represent that as guaranteed cleanup.
6. Cleanup and stale recovery may delete only artifacts created under the tool-owned attempt root;
   they must never delete the user's source cache.

## State transitions

```text
created -> policy evaluated
policy refused/missing/invalid -> failed
policy allowed -> credential injected or staged
injected/staged -> running
running -> completed | failed
completed/failed -> cleaned
parent terminated abruptly -> stale candidate
stale candidate -> expired only after safe marker/age/ownership checks
```

## Data sensitivity

Credential contents and source-cache paths are secret-sensitive. Reports may carry only the auth
mode, execution context, policy result, and cleanup classification. The source cache remains owned
by the operator's configured credential store; the attempt lifecycle owns only its temporary copy or
process environment.
