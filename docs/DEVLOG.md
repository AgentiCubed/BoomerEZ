# Devlog

Newest first. One entry per meaningful change. Say what changed and why it mattered.

---

## 2026-08-02 — Repository established

Brought the three foundation documents together into one place and gave the collection a home.

- Design Standard v1 and the Earl Rubric moved in as `docs/`, with the rubric split into its own file so it can be copied per gate and committed as a report.
- The 15-minute moderated test protocol and five-person persona panel filed under `docs/research/`. The relationship between Earl and the panel is now written down explicitly: Earl is the cheap filter that runs first, the panel is the actual evidence. Arthur Bell — confident, fast, and misled by our own wording — is the case Earl structurally cannot produce, since Earl is us reading our own screens.
- Mode Studio placed at `apps/mode-studio/index.html`, carrying Simple Mode.
- Landing page at the root, written to the same standard it advertises: 18px floor, one primary action per card, plain language, explicit reassurance.
- CI adapted from the hardened static-site workflow: errors-only HTML validation, plus structure checks that every app has an `index.html`, that the four governing documents exist, and that no audio or video is ever committed.
- `.gitignore` blocks media and session recordings by default. Participant recordings must never reach a public repository, and the safest place to enforce that is before the first mistake.

**Standing risk noted:** the product name has not been tested with the people it names. Rule 10 applies to it. Ask in the first real session.
