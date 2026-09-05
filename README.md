# BoomerEZ

[![Static Site CI](https://github.com/AgentiCubed/BoomerEZ/actions/workflows/ci.yml/badge.svg)](https://github.com/AgentiCubed/BoomerEZ/actions/workflows/ci.yml)

Software for capable adults who were never taught the vocabulary.

**The thesis:** the user brings the idea, the taste, and the details only they know. The software brings everything else.

Every program here is a single self-contained HTML file. No install, no account, no server, no data leaving the machine. Open it and it works — offline, on a ten-year-old laptop, on a tablet.

---

## The collection

| # | Program | What it does | Status |
|---|---------|--------------|--------|
| 1 | [Mode Studio](apps/mode-studio/) | Turns "what do you want the AI to do?" into a ready-to-paste command, and shows you exactly where to paste it | Simple Mode shipped; pre-ship gate pending |
| 2 | BoomerEZ Music | Takes a folder of your songs and turns it into a page you can share with family | Wireframe stage |

More to come. Each one starts from the same question: what does a person actually want to accomplish, and what is the software refusing to do for them?

---

## How to work here

Read these in order. They are the constitution of this repo, not decoration.

1. **[Design Standard](docs/DESIGN_STANDARD.md)** — the twelve rules. A screen either passes or it doesn't ship.
2. **[Earl Rubric](docs/EARL_RUBRIC.md)** — the ten-point pass/fail gate, applied at wireframe, first build, and pre-ship.
3. **[Usability Test Protocol](docs/research/usability-test-protocol.md)** — the 15-minute moderated test with real participants, plus the five-person persona panel. Earl catches problems early and cheaply; real people catch the ones Earl can't imagine.
4. **[Roadmap](docs/ROADMAP.md)** — phases, and what "done" means for each.
5. **[Agent Lanes](docs/AGENT_LANES.md)** — who writes what, and the one rule that keeps parallel work from colliding.

---

## Repository layout

```
apps/           one folder per program; each is a single self-contained index.html
docs/           design standard, rubric, roadmap, lanes, devlog
docs/research/  test protocol, persona panel, findings
docs/reports/   accessibility audits, test session records
packages/       shared design tokens and the rubric linter
tools/          build, bundle, and test scripts
```

**The lane rule:** app HTML files under `apps/` are authored in one place and consumed everywhere else. Tooling reads them, bundles them, audits them, and tests them — tooling never edits them. See [Agent Lanes](docs/AGENT_LANES.md).

---

## Running a program

Download the `index.html` for any app and double-click it. That is the whole procedure, and it is deliberate — the install step is where this audience is lost.

## License

MIT. See [LICENSE](LICENSE).
