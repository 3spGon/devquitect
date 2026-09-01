# Proportional Change Profile architecture

Status: Approved
Last updated: 2026-08-31

## Confirmed

- Gate 2 was explicitly approved in chat on 2026-08-31.
- The current baseline is summarized by [../system-context.md](../system-context.md) and verified by the declarative skill files, checkpoint contract, evaluation schema, and repository quality tooling.
- The implementation is declarative skill behavior plus behavioral test definitions; it does not introduce a runtime service or external dependency.

## Assumptions

- The current evaluation case schema and deterministic assertion engine are sufficient. Profile semantics can be graded through a focused rubric while Git cleanliness and forbidden effects enforce safety.

## Open decisions

No implementation-blocking architecture decisions remain.

## Current architecture

- `SKILL.md` orchestrates initiative classification, progressive definition, both approval gates, and handoff boundaries.
- References own detailed discovery, experience, technical-design, artifact, checkpoint, baseline, and planning contracts.
- `00-status.md` is the durable state owner for persistent sessions.
- YAML evaluation cases plus deterministic observations and optional semantic rubrics validate skill behavior.
- `project-plan-execution` consumes approved gates and plans without interpreting how they were produced.

## Proposed architecture

### Normative Change Profile reference

Create `skills/software-idea-to-project/references/change-profile.md` as the single normative owner of:

- vocabulary and invariants;
- provisional and confirmed lifecycle;
- evidence-based depth selection;
- expedited disqualifiers;
- elevation and invalidation;
- combined approval presentation and transition rules.

Other reference files link to this owner and describe only their local integration responsibilities.

### Workflow orchestrator

`SKILL.md` introduces profile establishment after initiative and baseline classification. It routes confirmed standard and full initiatives through the existing gates and allows the expedited combined request only under the normative preconditions.

### Contextual integrations

- `discovery.md` owns baseline, delta, preserved behavior, and initial confirmation inputs.
- `experience-design.md` maps interaction significance to affected surfaces and expedited disqualifiers.
- `technical-design.md` owns the architecture-impact test, Gate 2 readiness, and technical contradiction handling.
- `artifacts.md` defines where profile rationale and operational state live without adding a project artifact.
- `session-state.md` owns persistence, transition, compatibility, and invalidation rules.
- `implementation-planning.md` carries profile risks and proportional System Context refreshes into delivery slices.
- `agents/openai.yaml` may clarify proportional change analysis without changing the public skill name.

### Quality evidence

Focused cases under `evals/cases/` exercise expedited routing, risk elevation, stale context, legacy checkpoint compatibility, and the refactoring boundary. A profile-specific semantic rubric checks the response contract; deterministic assertions continue to enforce read-only and authorization effects.

## Data and control flow

```text
System Context + repository evidence
                 |
                 v
baseline + requested delta + preserved behavior
                 |
                 v
provisional Change Profile (safe default: standard)
                 |
                 v
surface, risk, architecture, and verification assessment
                 |
                 v
confirmed Change Profile
       |                              |
       v                              v
expedited eligibility          standard or full
       |                              |
       v                              v
combined Gate 1 + Gate 2       Gate 1 -> technical design -> Gate 2
       |                              |
       +---------------+--------------+
                       v
              implementation planning
```

## Gate transition contract

The expedited path remains in `crystallize` while it performs a bounded no-change architecture assessment. Before approval, both gates remain `pending` and the session is `awaiting-approval`. Explicit combined approval marks both gates approved and moves directly to `implementation-planning`.

If the assessment identifies any material architecture treatment, the profile elevates and returns to the sequential path; it does not enter detailed technical design before Gate 1.

## Failure and recovery behavior

- Missing or contradictory evidence fails closed to standard or full depth.
- `cross-cutting` always routes to full.
- Elevation is monotonic within the current evidence set; reducing depth never silently restores approval or deletes already required analysis.
- Repository evidence that changes only technical impact invalidates Gate 2. Evidence that changes approved behavior invalidates both gates.
- A legacy checkpoint with no profile is interpreted normally; the profile is established only during a relevant state-changing resume.
- Concurrent checkpoint updates continue using the existing revision re-read rule.

## Compatibility and boundaries

- No schema-version increment or mandatory migration.
- No modification to `project-plan-execution` or `targeted-refactoring`.
- No external network, credential, data, security, privacy, deployment, or availability boundary is introduced.
- The principal risks are semantic ambiguity, accidental gate bypass, overuse of expedited routing, and drift between duplicated instructions. A single normative reference, fail-safe defaults, explicit transitions, and behavioral cases treat those risks.

## Traceability

| Requirement group | Technical owner |
| --- | --- |
| REQ-001–REQ-007 | Change Profile reference, discovery integration, orchestrator |
| REQ-008–REQ-011 | Change Profile reference, checkpoint transitions, technical-design integration |
| REQ-012–REQ-015 | Artifact, checkpoint, planning, and System Context contracts |
| REQ-016–REQ-018 | Existing cross-skill boundaries and neutral reference contract |
| REQ-019–REQ-022 | Change Profile presentation rules and focused rubric |
