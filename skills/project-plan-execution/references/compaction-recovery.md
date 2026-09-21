# Compaction recovery contract

Use this contract whenever operational context may be missing: compactation, startup or resume,
handoff, clear/reset, or an equivalent loss of working context. The hook only points here; this
reference and `09-delivery-status.md` own recovery.

## Recovery sequence

1. Select exactly one `09-delivery-status.md` checkpoint. If none is active, continue normally.
   If several are plausible or any plausible candidate is malformed, stop and report ambiguity.
2. Re-read the selected checkpoint and confirm its session, approved plan, plan revision, and
   supported schema. An active v1/v2 checkpoint requires repository reconciliation before one
   coherent migration to v3; a status-only read never migrates it.
3. Read the current slice, execution frontier, and only the `required_context` paths named by the
   frontier and approved plan. Inspect current repository status, relevant diffs, named source or
   test paths, and pending verification evidence.
4. Compare checkpoint claims with repository reality. Preserve confirmed completed work, inspect
   and continue partial work, and do not repeat completed work without contradictory evidence.
5. Classify any disagreement before implementation continues. Reconcile it with one coherent
   checkpoint revision, or stop with the discrepancy exposed.
6. Resume only the checkpoint's current `next_action`. Refresh the frontier at a meaningful
   progress boundary; routine reads and individual commands do not require a checkpoint write.

Conversation, compacted summaries, stale prompts, and tool-log recollection are hints only. They
cannot establish authorization, acceptance, deferral, completion, or verification. The repository
and the checkpoint are the authorities, and neither is trusted blindly when they disagree.

## Outcomes and operator messages

- `resumed`: one supported checkpoint agrees with repository evidence; continue its exact action.
- `reconciled`: a checkpoint/repository discrepancy was classified and recorded in one coherent
  revision; continue only the resulting action.
- `blocked`: required evidence, runtime support, or a user-only decision is unavailable; report
  the concrete dependency and do not claim recovery.
- `ambiguous`: multiple checkpoints or a malformed plausible checkpoint prevent safe selection;
  stop and request the minimum explicit choice or repair.

Automatic recovery is unavailable when the hook is disabled, untrusted, timed out, fails, or the
required Python runtime is missing. Do not install dependencies or describe manual recovery as
automatic success. Use the same contract manually through `project-plan-execution`.

## Hook limits

The synchronous `SessionStart` handler matches only `source: "compact"`. It reads one JSON event,
uses only `hook_event_name`, `source`, and `cwd`, and searches immediate
`docs/software-design/*/09-delivery-status.md` paths below the detected repository root. It
does not read transcripts, plans, diffs, logs, or checkpoint bodies; it does not execute data,
access the network, write markers, or create another task-state file. Its JSON stdout is bounded
to 4096 UTF-8 bytes and its configured Codex context injection is bounded to 1200 characters.

The hook is independently executable and deterministic in this slice. Plugin packaging and
manifest integration are owned by `SLICE-003`; until then, the manual contract remains the
available recovery path.
