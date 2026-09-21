# Evaluation Authentication Governance

Status: Approved
Last updated: 2026-09-21

## Confirmed

- Devquitect has two materially different execution paths: credential-free structural checks and trusted model-backed behavioral evaluation.
- `devquitect eval`, `compare`, and `calibrate` currently discover the user's file-backed Codex login cache and pass it into the evaluation runner.
- The runner sets an isolated `CODEX_HOME` per attempt and stages `auth.json` into it with a final `0600` mode before invoking Codex.
- The staged file is removed in a `finally` block after normal subprocess completion or a handled child-process error.
- A parent-process `SIGKILL`, fatal crash, OOM termination, or unhandled terminating signal can leave the temporary root and staged cache behind.
- OpenAI's current Codex guidance states that signing in with an existing ChatGPT account applies the ChatGPT Terms of Use and Privacy Policy, while API and business users follow their corresponding agreement. The individual Terms of Use prohibit automatic or programmatic extraction of data or Output and bypassing rate limits or restrictions.

## Assumptions

- The first release continues to support behavioral evaluation, but authentication selection becomes explicit rather than inferred from a local login file.
- API-key or business-account authentication is the intended route for repeatable automated evaluation; the exact supported mechanism remains a technical-design decision.
- Local ChatGPT-cache execution may remain available for an operator-run diagnostic, but it is not assumed to be permitted for unattended or recurring evaluation loops.
- The initiative does not redesign case schemas, model selection, grading, comparison semantics, or release evidence beyond recording the selected authentication mode and its policy result.
- A filesystem cannot guarantee deletion after the process that owns the cleanup logic is forcibly killed; the design must state a best-effort guarantee and define stale-material recovery.

## Open decisions

None. `DEC-EAG-001` through `DEC-EAG-004` are resolved in [07-decisions.md](07-decisions.md);
the supervised-only boundary is now part of the approved design.

## Problem

The current toolchain treats a local ChatGPT login cache as an implementation convenience for
behavioral evaluation. That convenience crosses a sensitive credential boundary and can turn an
ordinary test command into an automated consumer-subscription client. The cleanup mechanism is
careful for ordinary failures but cannot provide a hard guarantee under forcible parent-process
termination. The repository therefore lacks a clear, enforceable contract for when subscription
authentication may be used, how credentials are staged, and what residual risk is accepted.

## Desired outcome

Behavioral evaluation has an explicit authentication policy and mode. The default structural path
remains credential-free. Automated evaluation uses only an approved authentication mechanism for
the execution context. Any local subscription-cache mode is visibly opt-in, bounded, and honest
about cleanup limitations. Reports retain the selected auth mode and policy outcome without
retaining secrets.

## System boundary

Inside this initiative:

- CLI authentication selection and default behavior for `eval`, `compare`, `calibrate`, and any
  behavioral `check` delegation;
- Codex adapter staging, permissions, cleanup, stale-artifact handling, and redaction;
- per-attempt `CODEX_HOME` lifecycle and evidence metadata;
- deterministic tests for auth policy, failure paths, and cleanup behavior;
- contributor documentation describing permitted execution modes.

Outside this initiative:

- changing OpenAI's Terms of Use or determining legal compliance on behalf of the user;
- redesigning the evaluation case schema or grading model;
- guaranteeing deletion after an operating-system-level kill of the parent process;
- building a hosted credential broker, secret manager, or CI service;
- changing the skills being evaluated.

## Actors and external systems

- **Maintainer or contributor** chooses an evaluation mode and is responsible for using an account and
  plan permitted for that mode.
- **Devquitect CLI** validates the requested auth mode, refuses disallowed implicit fallbacks, and
  records non-secret policy metadata.
- **Codex adapter** creates the isolated attempt, launches the trusted subprocess, and performs
  best-effort cleanup.
- **Operating system and filesystem** govern process signals, temporary directories, permissions,
  backups, and residual artifacts.
- **OpenAI Codex/ChatGPT or API service** authenticates the request, applies terms, quotas, and
  usage limits, and returns model-backed behavior.

## Primary workflow

1. The operator selects a behavioral command and an explicit authentication mode, or invokes the
   credential-free structural command.
2. The CLI validates that the mode is compatible with the execution context; no personal login
   cache is silently discovered.
3. The adapter creates a fresh attempt and isolated `CODEX_HOME`.
4. The selected credential is staged or injected using the narrowest supported mechanism, with
   permissions established at creation and no secret copied to reports or workspaces.
5. Codex runs within the existing sandbox and timeout boundaries.
6. Normal completion, timeout, child failure, and setup failure remove staged material and classify
   the result appropriately.
7. Abrupt parent termination is treated as a best-effort cleanup boundary; the next permitted run
   or an operator-maintained cleanup path handles stale material without reading or logging the
   credential.
8. The report records the auth mode, policy decision, runtime identity, and cleanup result without
   recording credential contents.

## Interaction surface

Minimal. There is no graphical interface. The consequential interactions are CLI flags, refusal
messages, explicit opt-in warnings, and report fields that tell the operator whether the run used
credential-free, API/business, or local subscription authentication. The experience must make an
implicit use of a personal subscription impossible to miss.

## Conceptual direction

Separate three concerns that are currently coupled:

```text
authentication policy
        -> selected credential mode
        -> isolated execution lifecycle
        -> non-secret evidence
```

The first implementation slice should prefer deleting implicit cache discovery over adding a
general authentication abstraction. A small explicit mode boundary is enough until a second
provider genuinely requires shared infrastructure.

## Change Profile

- Status: Confirmed
- Kinds: behavior change, technical change, deprecation
- Impact: Bounded
- Depth: Full
- Affected surfaces: behavior, interfaces, security/privacy, operations, quality attributes,
  migration/compatibility
- Elevation reasons: credential trust boundary, external usage policy, abrupt-termination recovery,
  and missing deterministic auth tests.

## Gate 1 proposal

Approve the purpose, boundary, primary workflow, minimal interaction surface, non-goals, and
full-depth Change Profile above. Approval authorizes detailed technical design only. It does not
authorize implementation, real model-backed tests, or automated use of a ChatGPT subscription.

References:

- [OpenAI Terms of Use](https://openai.com/policies/row-terms-of-use/)
- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
