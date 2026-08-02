# Agent Lanes

Several agents work on this repo in parallel. This document exists so none of them collide.

## The one rule

**App HTML under `apps/` is authored in one place and consumed everywhere else.**

Tooling reads app files, bundles them, audits them, tests them, and reports on them. Tooling never edits them. Break this rule and every parallel workstream turns into a merge conflict.

The boundary is drawn where the interface is stable: the app file is the artifact. Everything behind that interface — how tools process it — can change freely without coordination.

## Lanes

| Lane | Writes to | Reads | May edit app HTML? |
|------|-----------|-------|--------------------|
| **Authoring** | `apps/*/index.html`, `docs/*.md`, all user-facing copy | everything | Yes — exclusively |
| **Toolchain** | `tools/`, `packages/`, `.github/`, `docs/reports/` | app HTML, read-only | No |
| **Research** | `docs/research/` | published sources | No |
| **Backlog** | issues, templates, project board — scratch branches only | repo | No |

## Why the split falls this way

The authoring lane owns judgment calls: what a screen says, what order questions come in, whether a sentence condescends. Those are not parallelizable and not delegable — they are the product.

The toolchain lane owns everything mechanical and repeatable: bundling, linting, auditing, testing. This work compounds. A bundler written once works on every version of every app forever, which is why it is worth building before the apps that need it rather than after.

## Toolchain backlog

Work items for the toolchain lane, in dependency order:

1. **CI** — hardened HTML validation, errors-only, badge in README *(shipped)*
2. **Offline bundler** — `tools/build.py`: inline the drag library (pinned + SHA-256 verified) and the font as base64 `@font-face`; verify zero remaining external requests; fail CI if any remain
3. **Design tokens** — `packages/tokens/boomerez.css`: palette, type scale with 18px floor, spacing, focus rings
4. **Rubric linter** — `packages/earl-lint`: type size, contrast ratios, focus visibility, tap targets, color-only signaling, reduced motion. JSON + human-readable table. Warn first, fail later
5. **Validator test harness** — extract Mode Studio's chain validator by regex, run 60+ cases, assert the structural invariants (every goal chunk exists in the palette; every command covered by a task group; unique ids)
6. **Command-pack schema** — portable harness packs, a validator, and a merge tool that *prints* a snippet rather than injecting it
7. **Accessibility audit** — axe-core + Playwright at three viewports and both themes, output to `docs/reports/`

Items 2–7 all read app HTML and write only to their own directories. None of them can conflict with authoring or with each other.

## If a tool needs an app file changed

Open an issue describing the needed change and what it unblocks. The authoring lane makes the edit. This is slower than editing it directly, exactly once, and faster than every subsequent merge conflict.
