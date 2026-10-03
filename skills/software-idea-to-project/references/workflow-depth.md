# Workflow Depth

Use this reference for every software-definition initiative. Select and state a depth from impact, uncertainty, reversibility, and risk; do not use file count or a request for speed as the deciding factor.

## Select a depth

- **lightweight** — the scope is clearly bounded, low-risk, reversible, and needs no material product, domain, experience, or architecture decision.
- **standard** — ordinary discovery, design approval, technical confirmation, or planning is needed. Use this when evidence is incomplete or the choice between lightweight and rigorous is uncertain.
- **rigorous** — work is cross-cutting, hard to reverse, migration-heavy, trust-sensitive, compatibility-sensitive, or otherwise high-risk.

Apply the same selector to `new-system`, `system-change`, and `hybrid` initiatives. New-system work does not need a Change Profile. For system-change and hybrid work, retain the Change Profile and record the equivalent common depth at the checkpoint's top level: `expedited` maps to `lightweight`, `standard` to `standard`, and `full` to `rigorous`.

Explain the selected depth and its evidence in the conversation. If the initiative is persistent, record it as `workflow_depth` in `00-status.md`. A legacy checkpoint without that field defaults to `standard`, unless its existing Change Profile contains a depth that maps to the common value. Do not migrate or rewrite a legacy checkpoint for status-only work; record the effective value only during an ordinary state-changing update.

## Resolve a persistent definition root

Use one caller-supplied `definition_root` only when creating a new persistent session. It must be a normalized path relative to the repository root, must not traverse with `..`, and must resolve inside that repository. When no root is supplied, use `docs/software-design`. Store the selected root in each new `00-status.md`; the session lives at `<definition_root>/<slug>/`.

When resuming, use the checkpoint's recorded `definition_root` first. A newly supplied root never moves or silently copies an existing session. A legacy checkpoint without a root stays at its current path and is discovered under the default or other known session locations. If more than one viable checkpoint matches, present the candidates and ask the user which one to resume; do not choose by recency or search order.
