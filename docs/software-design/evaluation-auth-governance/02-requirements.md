# Evaluation Authentication Governance requirements

Status: Approved
Last updated: 2026-09-21

## Confirmed

- The existing structural check is credential-free and must remain so.
- Behavioral commands currently use a local ChatGPT login cache when `~/.codex/auth.json` exists.
- The current adapter already isolates each attempt's workspace, `CODEX_HOME`, skill root, and
  evidence namespace.

## Assumptions

- Requirements below describe the target contract, not implemented behavior.
- Authentication policy is evaluated before any credential is copied, opened, or injected.
- Reports may identify an auth mode and policy decision but never contain credential values or raw
  login-cache contents.

## Open decisions

None. The approved supervised-only boundary resolves the policy choice; implementation details are
constrained by [04-architecture.md](04-architecture.md) and [06-api-contracts.md](06-api-contracts.md).

## Functional requirements

### REQ-EAG-001 — Preserve the credential-free path

`devquitect check --source ...` without an explicit behavioral request must not discover, open,
copy, or use a ChatGPT login cache. A credential-free check must remain runnable without API keys,
ChatGPT login, or subscription access.

### REQ-EAG-002 — Make behavioral authentication explicit

Behavioral commands must receive an explicit authentication mode or a clearly documented
non-subscription default. The CLI must not silently fall back from an unavailable approved mode to
the user's local ChatGPT cache.

### REQ-EAG-003 — Gate unattended execution

The tool must distinguish operator-run local subscription evaluation from unattended or recurring
evaluation. A mode not approved for unattended use must fail closed with an actionable message
before staging credentials or starting Codex.

### REQ-EAG-004 — Isolate credentials per attempt

Any supported file-backed credential must be scoped to one attempt's `CODEX_HOME`, must not mutate
the source cache, and must not be copied into the workspace, evidence namespace, repository, or
report.

### REQ-EAG-005 — Establish restrictive permissions at creation

The staged credential must be created with owner-only permissions from creation rather than relying
only on a later `chmod`. The parent temporary directory and any credential-bearing descendants must
also have an explicitly verified ownership and permission policy.

### REQ-EAG-006 — Define cleanup guarantees honestly

Normal completion, timeout, handled setup failure, and child-process failure must remove staged
credentials. The documentation and report must not claim cleanup after `SIGKILL` or an equivalent
fatal parent-process termination unless an external supervisor provides that guarantee.

### REQ-EAG-007 — Recover stale material without exposing it

If crash recovery is supported, stale attempt directories must be identifiable without reading
credential contents, bounded by ownership/age/marker checks, and removed only within the tool's
explicit temporary root. Recovery must never delete the user's source cache.

### REQ-EAG-008 — Keep evidence non-secret and auditable

Reports must record the selected authentication mode, policy result, runtime identity, and cleanup
classification. They must not record tokens, cache contents, credential paths outside normalized
temporary identifiers, or raw authentication errors containing secrets.

### REQ-EAG-009 — Preserve model configurability

Authentication policy must remain independent from model and reasoning configuration. A test may
choose its model and reasoning effort without forcing a specific authentication provider beyond the
approved policy for that execution context.

## Acceptance scenarios

1. A normal structural check with `~/.codex/auth.json` present completes without opening or copying
   the cache, and its report identifies a credential-free run.
2. A behavioral command without an explicit permitted auth mode fails before credential staging when
   no safe default exists.
3. An explicitly permitted API/business-auth run uses only the supplied credential mechanism and
   leaves no credential material in the attempt workspace or report.
4. An explicitly permitted local subscription run displays its policy warning and records the mode
   without exposing the cache path or contents in evidence.
5. A child Codex process that exits non-zero, times out, or emits malformed output leaves no staged
   `auth.json` after the parent returns.
6. A staging permission failure cannot leave a readable partial credential in the isolated home.
7. A simulated stale attempt is removed only when it matches the tool's ownership, marker, and age
   policy; an unrelated directory and the user's source cache remain untouched.
8. A report remains useful after an auth refusal or cleanup failure and classifies the run as
   configuration/infrastructure failure rather than behavioral pass.

## Preserved behavior

- Structural validation, packaging, release checks, and ordinary fast tests remain credential-free.
- Existing evaluation case semantics, model/reasoning flags, sandbox restrictions, report envelope,
  and exit-code meanings remain unchanged except for the new auth-policy metadata and refusal paths.
- No implementation is allowed to infer that temporary storage makes a subscription loop compliant
  with external terms.

## Non-functional requirements

- Security/privacy: least-privilege credential access, no secret persistence by design, bounded
  redaction, and explicit residual-risk documentation.
- Reliability: cleanup must be deterministic for handled failures and stale recovery must be bounded
  and safe under retries.
- Compatibility: existing users of credential-free commands must not need new credentials; legacy
  behavioral invocations must either preserve behavior through an explicit migration path or fail
  with a clear upgrade message.
- Operability: an operator must be able to distinguish policy refusal, missing credentials, runtime
  failure, and stale-cleanup failure without inspecting secrets.
