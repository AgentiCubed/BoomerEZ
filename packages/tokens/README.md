# @boomerez/tokens

Shared CSS design tokens (`--bz-` prefix) for the BoomerEZ collection —
toolchain backlog item 3 (docs/AGENT_LANES.md).

`boomerez.css` codifies the palette, type scale (18px floor), spacing,
card shape, tap-target minimum, and focus-ring values **from the shipped
landing page and Mode Studio**. It is the single place those values live
going forward; apps adopt the custom properties when the authoring lane
chooses (tooling never edits app HTML).

The 18px floor and 44px tap minimum are the machine-checkable ends of Earl
checks 4 and 9 — `packages/earl-lint` warns when a page sits below them.
