# Mode Studio

Turns "what do you want the AI to do?" into a ready-to-paste command — and then shows you exactly where to paste it.

## For the person using it

Download `index.html` and double-click it. That's all.

The first screen asks what you'd like to do, in ordinary words. Pick one and you get your command, an explanation of every piece of it, and step-by-step instructions for where it goes — including which keys to press on a Mac or on Windows.

## For the person building it

Single self-contained HTML file. Twelve modes, one shared command database.

**Simple Mode** is the default view: 14 plain-English goals, 18px+ type, editable fields for the parts only you know, per-piece explanations in visible text (never hover), and literal terminal instructions closing the paste gap. Everything else is the advanced dashboard, one clearly labeled button away.

**The advanced dashboard** covers five harnesses — Ollama, llama.cpp, LM Studio, vLLM, and Claude Code — with a global harness switcher that re-scopes every mode at once. Modes: Control, Create, Speed, Launch, Edit, Zen, Explore, Train, Macro, Fill, Build.

### Invariants worth preserving

- **Index coverage is computed, not curated.** Every command must appear in a task group; the Explorer auto-generates an A-to-Z index and surfaces anything uncovered. Verify per-harness after adding commands.
- **Commands carry a `kind`.** Keyboard shortcuts (`Ctrl+D`, `Ctrl+C`, `Ctrl+L`) are `kind:'key'` — they display with a keyboard glyph, never copy to the clipboard, and are excluded from autocomplete and macro chains. A keypress is pressed, not pasted.
- **Chain validation is live.** The builder reports valid / incomplete / invalid with a plain-English explanation and a hint. Run the validator test suite after touching `analyzeChain`.
- **Destructive commands carry their warning before the command, not after.**

### Open items

See [the roadmap](../../docs/ROADMAP.md). Nearest: Earl Gate 2, offline bundling, reorder buttons in the builder, accessibility audit.
