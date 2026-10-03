# Devquitect Next requirements

Status: Approved
Last updated: 2026-09-22

## Confirmed

### R-01: Preserve authority boundaries

The three existing skills remain distinct: definition does not implement, plan execution does not invent architecture, and targeted refactoring does not disguise behavior changes as refactors.

### R-02: Lean entrypoints with cross-generation evidence

The 0.7.0 skill entrypoints state each policy once and preserve only outcome, constraints, authorization, readiness, escalation, and completion behavior that the agent needs at entry. Detailed state and artifact mechanics remain in their designated owners. Every material simplification is evaluated against the same representative cases before it is retained. GPT-5.6 remains a reproducible prior-generation baseline; the operating model is not tuned exclusively to that generation.

### R-03: QUICK route

0.7.0 adds an independently invocable skill that may activate implicitly when its precise description matches an authorized change that is localized, reversible, has no public-contract or material behavior decision, and has a direct verification path. It performs focused discovery, modifies only in-scope files, runs relevant validation, and reports the result concisely.

### R-04: QUICK escalation

QUICK must stop and route to the appropriate established workflow when evidence finds a feature decision, architecture decision, public contract, persistence or migration change, security-sensitive behavior, multi-module impact, or a need for durable continuity.

### R-05: Preserve delivered verification

The initiative does not modify `verify_slice.py`, its Python/PyYAML requirements, its YAML inventory, or the existing snapshot/check/close acceptance contract.

### R-06: Compatibility and stabilization

1.0.0 is eligible only after the new routes, escalation behavior, and retained verification boundaries have deterministic positive and negative coverage plus approved behavioral comparison evidence where authorized.

### R-07: Staged prompt-change protocol

Each material prompt simplification starts from an immutable baseline, changes one named rule group in one skill, reruns the same deterministic cases, and records a retain, move, or remove disposition. A behavioral comparison, when authorized, uses a declared model/host configuration and the same case set. Regression or inconclusive evidence retains the prior text.

### R-08: Prompt-change ledger

The repository maintains a versioned prompt-change ledger. Each entry identifies the immutable baseline and candidate snapshots, affected paths and rule groups, disposition, deterministic cases, model/host configuration when applicable, report references, and verdict. Source text is reconstructed from the referenced snapshots rather than duplicated in the ledger.

### R-09: Generalized workflow and persistence configuration

Workflow depth applies to every initiative according to impact and risk. Persistent definition work resolves a configured root when supplied and otherwise uses a detected repository default; existing sessions remain discoverable at their current paths.

### R-10: Invocation and evaluation policy

The invocation policy explicitly controls implicit activation for each skill. The initial evaluation matrix includes GPT-5.6 Sol, Terra, and Luna as baseline rows and GPT-6 Sol (`gpt-6-sol`) and GPT-6 Luna (`gpt-6-luna`) as separate new-generation rows. Each row declares model, host, runtime, reasoning effort where supported, suite revision, repetitions, and reports; results from different configurations are not pooled. Behavioral comparisons remain separately authorized.

## Assumptions

- No human interaction surface beyond skill invocation and textual results requires experience-design artifacts.

## Open decisions

- Confirm the stable ledger schema and approve the initial cross-generation model/host matrix described in R-10.
