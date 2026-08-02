# The Earl Rubric

The gate. Copy this file into a report for every gate you run, fill the result column, and commit it to `docs/reports/`.

**Who Earl is:** a composite reviewer, 68, retired, competent, owns a tablet he uses for photographs of grandchildren. He is not a real participant and never substitutes for one. He is the cheap check that runs before we spend a real person's fifteen minutes.

**When it runs:** three gates per program.

| Gate | When | Cost of a failure caught here |
|------|------|-------------------------------|
| 1. Wireframe | Before any code | Minutes |
| 2. First build | Before polish | Hours |
| 3. Pre-ship | Before a real user sees it | Days, plus a participant's goodwill |

**The standing rule:** nothing ships with an open FAIL.

---

## The ten checks

Read every screen aloud, in order, as Earl.

| # | Check | Pass condition | Result | Note |
|---|-------|----------------|--------|------|
| 1 | Five-second test | Earl says aloud what to do next within five seconds | | |
| 2 | Vocabulary | Zero undefined words; every unusual term defined in visible text on the same screen | | |
| 3 | Single action | Earl points at exactly one button when asked "what would you press?" | | |
| 4 | Legibility | Earl reads every word without leaning in | | |
| 5 | No dead ends | Earl knows what happens after the button, before pressing it | | |
| 6 | Cliff test | If the next step is outside our software, Earl can complete it from what we showed him | | |
| 7 | Fear check | Earl is not worried about breaking something | | |
| 8 | Recovery | Earl can get back after a wrong turn without starting over | | |
| 9 | Motor check | Every action completes with one imprecise click; no drag required | | |
| 10 | Dignity check | Nothing talks down to Earl or implies he should already know something | | |

---

## What a linter can and cannot do

Checks 4, 9, and the mechanical portions of 2 and 3 are machine-checkable: type size, contrast ratios, focus visibility, tap-target dimensions, color-only signaling, reduced-motion compliance. Those live in `packages/earl-lint` and run in CI.

Checks 1, 5, 6, 7, 8, and 10 are judgment. They stay human, and check 10 stays human permanently — a linter cannot detect condescension.

---

## Earl is not the test

Earl is a filter, not evidence. He catches the obvious before it wastes a real participant's session. The actual evidence comes from the [15-minute moderated protocol](research/usability-test-protocol.md) and its five-person panel, each of whom fails differently than Earl does:

| Persona | The failure Earl will never catch |
|---------|-----------------------------------|
| Nora Ellis | Understands the task perfectly, cannot reliably hit the target |
| Luis Mendoza | Navigates confidently until magnification breaks the layout |
| Elaine Parker | Understands more than she trusts herself to act on |
| Arthur Bell | Moves fast and confidently in the wrong direction, misled by our own words |
| June & Tasha Taylor | One goal, two people, control split between them |

Arthur is the sharpest argument for running real sessions: confidence hiding a wrong mental model looks like success from the outside, and Earl — who is *us*, reading our own screens — will never produce it.

---

## Report template

```
# Earl Gate — [program] — [gate 1/2/3] — [date]

Screens reviewed: [list]

[rubric table with results]

FAILS (must close before ship):
- [check #] [screen] — [what Earl said]

WARNINGS (fix or justify):
- [check #] [screen] — [what Earl said]

Verdict: PASS / PASS WITH CONDITIONS / FAIL
```
