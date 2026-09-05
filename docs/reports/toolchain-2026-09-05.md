# Toolchain report — 2026-09-05

Toolchain lane. Backlog items 2–4 from `docs/AGENT_LANES.md` land at their
first working increment, ported and adapted from the scaffold previously
staged in `AgentiCubed/A3:boomerez/` (PR #104 there), which this supersedes.

## Shipped

- **`tools/build.py` — offline bundler (item 2).** Copies the landing page
  and apps into `dist/`, inlines Sortable 1.15.2 (pinned,
  SHA-256-verified: `ca68430703c4f596…`, computed from the npm dist file
  that cdnjs/jsdelivr mirror; any mismatch aborts the build) and the
  JetBrains Mono stylesheet as base64 `@font-face` (latin subset), then
  fails the build if any external resource request remains. CI runs it, so
  a stray external reference fails CI. `BOOMEREZ_VENDOR_DIR` supports fully
  offline builds.
- **`packages/tokens/boomerez.css` — design tokens (item 3).** Palette,
  type scale (18px floor), spacing, card shape, 44px tap minimum, and
  focus-ring values codified from the shipped landing page and Mode
  Studio. Apps adopt them when the authoring lane chooses.
- **`packages/earl-lint` — rubric linter (item 4).** Static
  machine-checkable slice of the Earl Rubric: baseline structure (checks
  2/3 mechanical), 18px font floor (check 4), drag/tap-target signals
  (check 9), reduced-motion and `:focus` support. Warn-first as specified:
  table + JSON output, exit 0 without `--strict`. Contrast, rendered
  geometry, and color-only signaling wait for the browser audit (item 7).
- **`tools/run_tests.py`** — network-free suite covering structure, token
  integrity, rubric config, `.gitignore` coverage, and the bundler's
  external-request detector; CI job `toolchain` runs suite → lint →
  bundle → uploads `dist/` as an artifact.

## Current earl-lint findings (expected, warn-only)

- Mode Studio: font sizes below the 18px floor (dense editor chrome) and a
  drag interaction (Sortable) — both known, gated by the warn-first policy
  until the authoring lane addresses them or the policy flips to strict.

## Notes for the authoring lane

- `README.md` badge now points at this repo (`AgentiCubed/boomerez`) —
  it previously pointed at `JamesTRichmond/BoomerEZ`.
- The landing page's "See how it's built" link also points at
  `JamesTRichmond/BoomerEZ`; that's app HTML, so it stays untouched by
  this lane. Issue-worthy if the repo's home is settled here.
- `PUSH_ME.md` removed: its own instruction ("delete this file once it's
  pushed") plus the fact the repo it described is live.
