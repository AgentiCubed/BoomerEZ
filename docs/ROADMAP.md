# Roadmap

## Phase 0 — Foundation ✅

- [x] Design Standard v1 — the twelve rules
- [x] Earl Rubric — the ten-point gate
- [x] Usability test protocol + five-person persona panel
- [x] Repository established
- [ ] Domains: BoomerEZ.ai and BoomerEZ.com

## Phase 1 — Mode Studio, final iteration

**Done means:** a first-time user opens the file, picks a plain-English goal, gets a working command, and successfully pastes it into a terminal without outside help.

- [x] Simple Mode as the default screen — 14 plain-English goals, 18px+ type, editable command, per-piece explanations in visible text
- [x] The cliff closed — literal Mac and Windows instructions for finding the terminal and pasting
- [x] Chat-vs-terminal distinction stated explicitly
- [x] Cautions on destructive commands, shown before the command
- [ ] Earl Gate 2 (first build) on all Simple Mode screens
- [ ] Offline bundling — inline the drag library and font, zero external requests
- [ ] Reorder buttons in the advanced builder (rule 6: nothing requires drag)
- [ ] Accessibility audit at three viewports, both themes
- [ ] Earl Gate 3 (pre-ship)
- [ ] Two real 15-minute sessions with participants 65+

## Phase 2 — BoomerEZ Music

**Done means:** a person with a folder of song files ends up with a link they can send to their family, having never seen a terminal, an account signup, or the word "deploy."

- [ ] Wireframe → Earl Gate 1
- [ ] Wizard build: find the songs → hear them → describe them → make the page → share it
- [ ] Three share paths: email it, put it on a USB stick, put it on the internet
- [ ] The internet path uses drag-a-folder-onto-a-webpage hosting — no terminal, no account complexity, no code
- [ ] Earl Gates 2 and 3
- [ ] Real sessions

**Architecture:** single self-contained HTML, fully client-side. The music never touches a server we run. This is a hard requirement, not a preference — it is also the honest answer to "where do my songs go?"

## Phase 3 — Series infrastructure

- [ ] Shared design tokens in `packages/tokens`
- [ ] Rubric linter in `packages/earl-lint`
- [ ] Offline bundler and test harness in `tools/`
- [ ] Landing page presenting the collection — which passes the rubric like everything else

---

## Standing decisions

**Single-file HTML, always.** The install step is where this audience is lost. Every program must survive being emailed as an attachment and double-clicked.

**Offline by default.** A program that needs a working internet connection to render is a program that fails in a farmhouse in Vermont.

**Simple is the default view, not a mode you find.** The expert dashboard lives behind one clearly labeled button. Inverting this — expert by default, simple as an option — is how every product this audience has abandoned was built.

**The name is not settled.** "BoomerEZ" reads warm to some of this demographic and condescending to others. Rule 10 applies to the product name. Ask it in the first real session and be willing to hear the answer.
