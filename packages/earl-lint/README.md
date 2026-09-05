# @boomerez/earl-lint

Static rubric linter — toolchain backlog item 4 (docs/AGENT_LANES.md),
implementing the machine-checkable slice of [the Earl Rubric](../../docs/EARL_RUBRIC.md).

```sh
python3 packages/earl-lint/earl_lint.py index.html apps        # lint the site
python3 packages/earl-lint/earl_lint.py --json out.json apps   # + JSON report
python3 packages/earl-lint/earl_lint.py --strict apps          # findings fail
```

**Policy: warn first, fail later.** Findings print as a human-readable table
(and optional JSON) but exit 0; CI stays green while the apps converge on the
standard. Flip to `--strict` in CI when the time comes.

What it checks statically: baseline document structure (doctype, `lang`,
title, viewport, `img` alt — the mechanical portions of Earl checks 2/3),
font sizes below the 18px floor (check 4), drag interactions and missing
44px tap-target minimums (check 9), and reduced-motion / `:focus` support
from the design standard. Contrast ratios, rendered tap-target geometry, and
color-only signaling need a rendering engine — they arrive with the
browser-based audit (backlog item 7).

Rules live in `rubric.json`; each maps to a check in `earl_lint.py` and
names the Earl check it serves. The linter only ever **reads** app HTML.
