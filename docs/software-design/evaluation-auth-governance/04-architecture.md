# Evaluation Authentication Governance architecture

Status: Approved
Last updated: 2026-09-21

## Confirmed

- The current architecture has CLI command handlers, a shared evaluation runner, Codex adapters,
  temporary fixture attempts, normalized observations, and report builders.
- `run_codex` already owns the subprocess boundary and isolated `CODEX_HOME`; `run_app_server`
  owns the App Server lifecycle path.
- The current implementation autodiscovers the user's login cache in the CLI and stages it in the
  adapter.

## Assumptions

- The existing Python stack, report envelope, attempt isolation, sandbox flags, and exit semantics
  remain the foundation.
- A small policy boundary is sufficient; a general provider plugin system is not justified by the
  current number of authentication modes.
- The first stale-artifact mitigation is an in-process startup scavenger with strict ownership,
  marker, and age checks. It is a recovery aid, not a SIGKILL guarantee.

## Open decisions

None. The approved boundary prohibits `chatgpt-cache-local` in unattended execution.

## Current architecture

```text
CLI command
  -> discover_auth_cache() [implicit today]
  -> evaluation.run_case()
  -> codex_adapter.run_codex() or app_server_adapter.run_app_server()
  -> isolated FixtureAttempt.CODEX_HOME
  -> normalized Observation -> report
```

The current implicit discovery is the boundary to remove. The structural `check` path remains
outside this behavioral authentication flow.

## Proposed architecture

```text
CLI command + explicit auth options
  -> AuthPolicy.evaluate(mode, execution_context, environment)
  -> Evaluation runner
       -> credential-free path
       -> API/business environment injection
       -> explicitly permitted local cache staging
  -> isolated attempt lifecycle
       -> Codex exec or App Server adapter
  -> non-secret AuthDecision/CredentialState metadata
  -> Observation/report
```

### Components and responsibilities

| Component | Responsibility | Change |
| --- | --- | --- |
| CLI parser | Accept explicit auth mode and source options; reject ambiguous combinations | changed |
| Auth policy boundary | Decide whether a mode is allowed for the execution context before touching credentials | new small module or existing adapter helper |
| Evaluation runner | Pass the selected policy result and credential source to the chosen adapter | changed |
| Codex/App Server adapters | Inject or stage only the credential approved by policy; never autodiscover it | changed |
| Attempt lifecycle | Own marker, lock/liveness metadata, temporary root, and cleanup classification | changed |
| Report builder | Record non-secret auth metadata and cleanup status | changed |
| Structural check | Continue without auth policy or credential access | unchanged |

### Trust boundaries

1. The operator's source credential store is outside the tool-owned attempt root.
2. The CLI policy boundary is trusted to decide whether the requested mode is allowed, but it must
   not read credential contents to make that decision.
3. The isolated attempt root is a temporary sensitive zone visible to the trusted subprocess only.
4. The Codex process is an external service client; its stdout/stderr are untrusted and redacted
   before evidence retention.
5. Reports and repositories are non-secret zones and must never receive credential material.

### Credential lifecycle

- `credential-free`: do not discover or open any login cache.
- `api-key`: pass only the explicitly selected environment credential to the trusted subprocess;
  include its value in the redaction set, not in report data.
- `chatgpt-cache-local`: require an explicit path or opt-in flag; verify source ownership, regular-file
  status, symlink rejection, and restrictive source mode; create the destination with owner-only
  permissions from creation; wrap staging and execution in one cleanup scope.
- On handled completion or failure, unlink the staged file and remove the attempt root through the
  existing owner. On parent death, leave no false guarantee: a later scavenger may remove only
  tool-marked, old, non-live attempt roots.

### Stale cleanup

Each attempt that can contain credentials receives a tool-owned marker containing a random attempt
identifier, creation time, owning process identity, and schema version. Cleanup considers only the
known temporary parent and markers created by this tool. It requires an age greater than the maximum
configured attempt timeout plus grace, verifies that the owner is no longer live when the platform
permits that check, and refuses ambiguous or malformed entries. Concurrent active attempts must be
protected by a liveness marker or lock so a scavenger cannot remove a live run.

### Failure and compatibility behavior

- Policy refusal is a configuration failure before Codex launch.
- Missing or invalid credentials are configuration failures and do not retry automatically.
- Child exit, timeout, malformed output, and cleanup failure preserve the existing inconclusive
  infrastructure classification unless the report contract needs a more specific non-passing code.
- Existing credential-free invocations keep their current behavior.
- Existing behavioral invocations that relied on implicit cache discovery require a migration message
  and explicit auth selection; silent compatibility fallback is rejected.

## Alternatives considered

### Keep implicit cache discovery

Rejected. It preserves the current external-policy ambiguity and makes a credential-bearing side
effect invisible to callers.

### Remove all ChatGPT-cache support immediately

Safer policy boundary, but potentially breaks legitimate local diagnostic workflows. The approved
design keeps it as an explicit local-only option; any future expansion to unattended use requires a
new policy review and gate.

### Build a general authentication-provider framework

Rejected for now. Two concrete modes do not justify factories, plugin registries, or provider
interfaces. Add a shared abstraction only when a second supported provider needs behavior the small
policy boundary cannot express.

## Operational qualities

- Security/privacy: least privilege, no implicit subscription use, owner-only staged files, bounded
  redaction, and explicit residual-risk documentation.
- Reliability: cleanup is deterministic for handled failures; stale recovery is bounded and
  conservative.
- Observability: reports expose mode, context, decision, runtime, and cleanup classification only.
- Recovery: abrupt parent termination is recoverable on a later run when the marker/age/liveness
  checks are conclusive; otherwise the artifact is left for operator review.
- Rollback: revert the CLI policy and adapter changes together; existing credential-free checks are
  unaffected, while explicit behavioral callers must retain their selected auth mode.

## Traceability

| Requirement | Architecture treatment |
| --- | --- |
| REQ-EAG-001 | Structural check remains outside `AuthPolicy`; credential-free mode never discovers cache |
| REQ-EAG-002/003 | Explicit CLI mode plus policy evaluation before staging |
| REQ-EAG-004/005 | Attempt lifecycle and owner-only creation in the adapter boundary |
| REQ-EAG-006/007 | Single cleanup scope plus conservative stale scavenger |
| REQ-EAG-008 | Non-secret report metadata and redaction boundary |
| REQ-EAG-009 | Auth policy is independent from model/reasoning options |
