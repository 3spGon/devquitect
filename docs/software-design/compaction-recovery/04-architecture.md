# Compaction Recovery architecture

Status: Approved
Last updated: 2026-09-19

## Confirmed basis

- Gate 1 was explicitly approved on 2026-09-19.
- Codex runs a matching synchronous `SessionStart(source="compact")` hook before the next
  model request, including after automatic mid-turn compactation.
- Plugin hooks may be declared by `.codex-plugin/plugin.json`, receive `PLUGIN_ROOT`, and are
  skipped until their exact current definition is trusted.
- The repository already treats `09-delivery-status.md` as durable delivery state and the
  working tree as implementation reality.
- Current checkpoints use schema versions 1 and 2. The current slice verifier preserves
  unknown top-level fields while rewriting a checkpoint, but does not validate its version.
- The current package builder admits only `.codex-plugin/plugin.json` and `skills/**`.
- The current `codex exec` evaluation adapter cannot initiate or observe real compactations;
  Codex App Server can through `thread/compact/start` and `contextCompaction` events.

## Assumptions

None. Python 3.12+ is an explicit prerequisite of automatic recovery, not an inferred host
capability. If it is unavailable, the hook cannot claim that recovery ran.

## Open decisions

No blocking technical decision remains. These decisions become approved only at Gate 2.

## Minimal architecture

```text
Codex compactation
      |
      v
plugin SessionStart hook ---- zero candidates ----> silent continuation
      |
      +---- one active checkpoint ----> bounded recovery directive
      |
      +---- many/malformed candidates -> bounded ambiguity directive
                                             |
                                             v
project-plan-execution recovery contract
      |
      +---- read checkpoint and approved plan relation
      +---- inspect relevant repository evidence
      +---- read only frontier-required context
      +---- reconcile, then resume or report discrepancy
```

There is no marker, daemon, database, transcript parser, or second task-state file. The hook
only discovers a candidate and injects the recovery instruction. The skill owns recovery;
the checkpoint owns declared progress; the repository owns what actually exists.

## Components and ownership

| Component | Responsibility |
| --- | --- |
| `.codex-plugin/plugin.json` | Declare exactly `./hooks/hooks.json` in addition to the existing skills root |
| `hooks/hooks.json` | Register one synchronous `SessionStart` handler with matcher `^compact$` |
| `hooks/compaction_recovery.py` | Parse the event, discover active checkpoints, and emit bounded context without writes |
| `references/compaction-recovery.md` | Define compactation/resume reconciliation and operator-visible outcomes |
| `references/delivery-state.md` | Own schema v3, frontier semantics, legacy reads, and conservative migration |
| `references/execution.md` | Own milestone refresh cadence and the resume-before-implementation sequence |
| `verify_slice.py` | Refuse unsafe active legacy closure and preserve/validate the v3 frontier |
| quality packaging/validation | Admit and validate only the two declared hook files; keep deterministic artifacts |
| App Server eval path | Exercise real one/two/four compactation scenarios when model-backed testing is authorized |

The new critical authority contract `project-plan-execution.compaction-recovery` will use
`hooks/compaction_recovery.py` as the deterministic owner, with the recovery reference as
`explains`, the skill entrypoint as `routes`, and external cases/tests as `tests`. Existing
delivery-state and execution owners remain unchanged and receive their respective rules.

## Runtime hook

The handler is synchronous, has `timeout: 10`, and uses
`additionalContextLimit: 1200`. The script independently caps serialized stdout at 4096 UTF-8
bytes, so Codex spilling is not part of normal operation. These values are product limits and
must be deterministic tests, not environment guesses.

The hook is individually controllable through Codex's native hook browser (`/hooks`). An
operator may disable it without deleting plugin files or disabling unrelated hooks, and may
later enable it by reviewing/trusting the current definition there. Codex owns and applies that
runtime choice; Devquitect adds no sentinel, preference file, or duplicate enablement state. A
disabled hook is a supported operating mode, but automatic compactation recovery is
then unavailable and must never be reported as active. Manual skill-level resume remains.

The command uses the packaged script through `PLUGIN_ROOT`: POSIX invokes `python3`; Windows
uses `commandWindows` with `py -3`. It uses only Python's standard library. The implementation
must not install a runtime, access the network, read the transcript, execute checkpoint data,
or mutate the workspace.

Discovery starts at the hook input `cwd`, finds the containing workspace root using repository-
local markers, and inspects only immediate
`docs/software-design/*/09-delivery-status.md` candidates. A checkpoint is active when its
frontmatter identifies `skill: project-plan-execution` and its delivery phase is not terminal.
Candidate paths are normalized, repository-relative, sorted, and must remain inside the root.

The script needs only a constrained top-level YAML reader for known scalar fields. It does not
implement general YAML and does not need PyYAML. Unknown syntax in a plausible checkpoint is a
malformed-candidate outcome, never a reason to silently declare no active delivery.

Exit `0` with no stdout means no active delivery. One candidate emits JSON with
`hookSpecificOutput.hookEventName: SessionStart` and a short `additionalContext` naming its
path. Several or malformed candidates emit the same shape with an explicit stop-and-resolve
instruction. Invalid hook input or unavailable runtime is surfaced by Codex as a hook failure;
it is never described as successful recovery.

## Recovery sequence

All loss-of-operational-context signals use one sequence:

1. select exactly one checkpoint or stop on ambiguity;
2. validate its plan relationship and current schema support;
3. migrate an active v1/v2 checkpoint to v3 only after repository reconciliation;
4. read the current slice and execution frontier;
5. inspect only named paths plus relevant `git diff`/status and pending verification evidence;
6. compare checkpoint claims with repository reality;
7. preserve confirmed completed work, continue partial work, or report a discrepancy;
8. refresh one coherent checkpoint revision at the next meaningful progress boundary.

Conversation and compacted summaries are hints only. They cannot establish verification,
acceptance, authorization, completion, or deferral.

## Packaging and structural validation

The immutable source collector and package builder add only these root paths:

- `hooks/hooks.json`
- `hooks/compaction_recovery.py`

Both must be regular files; symlinks and undeclared files under `hooks/` are rejected. The
validator requires the manifest pointer to equal `./hooks/hooks.json`, checks the event,
matcher, synchronous command handlers, POSIX/Windows script targets, timeout, and context
limit, and rejects escaping paths or extra handlers. Existing sorted entries, stable timestamps,
source immutability, reproducible bytes, and digest behavior remain unchanged.

## Behavioral evaluation architecture

Existing ordinary cases continue through the `codex exec` adapter. Cases that declare
compactation lifecycle steps use a dedicated App Server adapter over stdio JSON-RPC. The
adapter starts an isolated workspace and isolated `CODEX_HOME`, validates packaged sources,
then may use `--dangerously-bypass-hook-trust` only inside that disposable evaluation boundary.

For every compact step it calls `thread/compact/start`, waits for the matching
`contextCompaction` `item/completed`, then starts the next turn. Evidence includes model/tool
events and resulting checkpoint/repository state. Required scenarios cover one, two, and four
compactations, stale conversation, partial implementation, and checkpoint/repository conflict.
No behavioral run is authorized by this design; repository policy still requires explicit
user authorization and its stable model/runtime calibration.

## Compatibility, rollout, and rollback

- Completed v1/v2 checkpoints remain unchanged and readable.
- Active v1/v2 checkpoints migrate on resume/update, never from a status-only read.
- New checkpoints start at v3.
- Missing legacy frontier facts remain empty/unknown until repository inspection; migration
  does not backfill claims from conversation.
- The slice verifier may inspect legacy state, but active close/update requires migration and
  reconciliation first.
- Hook installation/update requires trust review because Codex hashes the exact definition.

Operational rollback can disable or remove the hook without damaging checkpoints; skill-level
manual resume remains. Schema v3 reader support must remain after any rollback once an active
checkpoint has migrated. Downgrading to a version that cannot read v3 is not a supported or
safe rollback path.

## Failure boundaries

| Condition | Required behavior |
| --- | --- |
| Hooks disabled, untrusted, timed out, or failed | Codex warning/failure remains visible; do not claim automatic recovery |
| Python unavailable | Automatic recovery unsupported; no automatic installation |
| No active checkpoint | Silent no-op |
| Multiple active checkpoints | List bounded sorted candidates; do not choose |
| Malformed plausible checkpoint | Report recovery ambiguity; do not treat it as absent |
| Checkpoint/repository disagreement | Stop normal implementation until classified and reconciled |
| Oversized candidate set | Truncate safely within 4096 bytes and report omitted count |

## Traceability

| Requirements | Technical treatment |
| --- | --- |
| REQ-CR-001–004 | One v3 checkpoint, non-duplicating frontier, milestone refresh |
| REQ-CR-005–010 | Shared recovery sequence with repository reconciliation and ambiguity stop |
| REQ-CR-011–015 | Synchronous native hook, bounded output, zero/one/many behavior, no marker |
| REQ-CR-016–017 | Trust guidance and four concise operator outcomes |
| REQ-CR-018–020 | Exact hook allowlist, deterministic package, legacy read/migrate policy |
| REQ-CR-021–024 | Dual output bounds, local evidence, stdlib runtime, single-writer preservation |

## Gate 2 proposal

Gate 2 should approve this architecture, the v3 data model, the runtime/package/evaluation
contracts, and the compatibility limits. Approval authorizes implementation planning only; it
does not authorize implementation, publication, or model-backed evaluation.
