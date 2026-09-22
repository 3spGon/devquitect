# Compaction Recovery interface contracts

Status: Approved
Last updated: 2026-09-19

## Plugin manifest

The plugin manifest adds exactly:

```json
{
  "hooks": "./hooks/hooks.json"
}
```

The existing manifest fields remain unchanged. The referenced path must resolve inside the
plugin root and be included in the deterministic package.

## Hook configuration

The single supported handler has this semantic contract:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "^compact$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$PLUGIN_ROOT/hooks/compaction_recovery.py\"",
            "commandWindows": "py -3 \"%PLUGIN_ROOT%\\hooks\\compaction_recovery.py\"",
            "timeout": 10,
            "additionalContextLimit": 1200
          }
        ]
      }
    ]
  }
}
```

Implementation must verify the final quoting against Codex's documented command execution on
each platform; tests assert that both commands resolve only the packaged script. There is no
`async`, `PostCompact`, `PreToolUse`, or second handler.

## Activation contract

The packaged handler is configured when the plugin is enabled, but it runs only while Codex
considers that exact hook definition trusted and enabled. The operator uses Codex `/hooks` to:

- inspect the plugin source and command;
- trust/enable the current hook definition;
- disable this handler independently of Graphify and other hooks;
- re-enable it after review, including after an update changes its trust hash.

This control is independent of optional local developer tooling. No Devquitect CLI, environment
variable, repository marker, or mutable plugin file is introduced for activation.
The product documentation must state that disabled/untrusted means manual recovery remains
available but automatic compactation recovery does not.

## Hook input and output

The script accepts one JSON object from stdin. It uses only:

- the event identity/source needed to confirm `SessionStart` and `compact`;
- `cwd` to locate repository-local checkpoint evidence.

Other documented event fields are ignored. Non-object JSON, wrong event/source, missing or
invalid `cwd`, or paths outside the discovered root never trigger checkpoint recovery.

Outcomes:

| Outcome | stdout | exit |
| --- | --- | --- |
| Valid compact event, no active checkpoint | empty | 0 |
| Exactly one valid active checkpoint | hook-specific JSON with bounded recovery directive | 0 |
| Multiple or malformed plausible checkpoints | hook-specific JSON with bounded stop/resolve directive | 0 |
| Invalid input or unexpected runtime failure | no success context; concise stderr | non-zero |

Successful JSON shape:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "..."
  }
}
```

`additionalContext` contains the normalized checkpoint path(s), the command to enter the
project-plan-execution recovery contract, and the invariant that implementation cannot resume
before checkpoint/repository reconciliation. It contains no checkpoint body, plan body,
transcript, Git diff, secrets, or tool logs. Serialized stdout is at most 4096 UTF-8 bytes.

## Checkpoint discovery contract

Input `cwd` must exist below one repository root. Discovery examines only immediate session
directories under `docs/software-design/`. Candidate selection uses known top-level scalar
frontmatter keys and rejects duplicate keys for those fields. Results are unique, normalized,
repository-relative, and sorted.

Terminal delivery statuses are those already defined by project-plan-execution. The
implementation must reuse that vocabulary rather than introduce a second status enum. A file
that plausibly identifies the delivery skill but cannot be safely classified is malformed and
forces ambiguity.

## Skill recovery contract

Given one selected checkpoint, the skill returns one of four observable outcomes:

- **resumed:** checkpoint and repository agree; the exact partial/next action may continue;
- **reconciled:** a discrepancy was resolved and one coherent checkpoint revision records it;
- **blocked:** a concrete mismatch, missing approval/runtime, or verification problem prevents
  implementation;
- **ambiguous:** more than one checkpoint or interpretation needs an explicit selection.

The outcome is prose in the normal task, not another persisted status file. Only the existing
checkpoint changes when a coherent state transition is justified.

## Packaging and validation interfaces

The source collector accepts the existing inputs plus the two exact hook paths. Validation
errors must identify at least these categories: manifest pointer missing/wrong, hook config
malformed, event/matcher wrong, asynchronous handler, unsupported handler, command escapes
plugin root, platform command missing, bounds missing/wrong, undeclared hook file, symlink, and
non-regular file.

Package APIs and output schemas do not change. Adding or changing either declared hook file
changes the package digest; two builds from identical source remain byte-identical.

## Behavioral case extension

Existing eval cases with `turns: [string, ...]` remain valid and continue through `codex exec`.
A case may instead declare a versioned lifecycle scenario:

```yaml
scenario:
  schema_version: 1
  adapter: codex-app-server
  steps:
    - prompt: "Begin the approved delivery and stop after the requested boundary."
    - compact: {}
    - prompt: "Continue."
```

Each step has exactly one key. `prompt` is a non-empty string. `compact` is an empty mapping;
it is invalid before a thread exists or while a prior turn/compact event remains incomplete.
`turns` and `scenario` are mutually exclusive. Unknown adapters, steps, or versions fail schema
validation rather than silently falling back.

The App Server adapter:

1. starts the repository-controlled Codex adapter in an isolated evaluation environment;
2. sends prompt turns through the existing evaluation policy;
3. sends `thread/compact/start` for every compact step;
4. waits for the same-thread `contextCompaction` `item/completed` before the next step;
5. records lifecycle events, model/tool actions, filesystem state, and checkpoint revisions;
6. fails on timeout, wrong-thread events, hook failure, or out-of-order lifecycle.

This is a separate adapter because concatenating prompts into one `codex exec` invocation
cannot prove that compactation occurred. It is not a general workflow engine: only prompt and
compact steps are in scope for the approved scenarios.

## Compatibility and security

- Hook trust bypass is forbidden in normal use. It may be enabled only by the evaluator inside
  a fresh disposable environment after validating package source.
- Normal activation/deactivation uses Codex's individual hook control. Disabling the global
  hooks feature or the whole plugin also prevents execution, but is not the recommended control
  because it affects unrelated capabilities.
- No hook path consumes network data, transcript formats, or executable checkpoint content.
- No secret-bearing environment values are emitted.
- App Server `thread/shellCommand` is not used by the evaluator because it runs outside the
  thread sandbox; repository inspection remains ordinary model tool activity under test.
- Unsupported runtimes and disabled/untrusted hooks are explicit failures, not a manual-success
  fallback.

## Acceptance mapping

| Scenario | Required evidence |
| --- | --- |
| ACC-CR-001/002 | Real `contextCompaction` events at counts 1, 2, and 4; no repeated completed work |
| ACC-CR-003 | Stale prompt loses to checkpoint plus repository evidence |
| ACC-CR-004 | Existing partial paths inspected and continued, not overwritten/restarted |
| ACC-CR-005 | Contradiction exposed before implementation resumes |
| ACC-CR-006/007 | Deterministic hook no-op and bounded ambiguity outputs |
| ACC-CR-008 | Disabled/untrusted/failed hook never reports successful automatic recovery |
| ACC-CR-009 | Structural validation, exact contents, reproducibility, and digest tests |
