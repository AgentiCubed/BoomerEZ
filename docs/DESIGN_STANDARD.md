# BoomerEZ Design Standard v1

The rulebook for every program in the BoomerEZ collection. A screen either passes or it doesn't ship.

**Who we build for:** a capable adult with decades of hard-won judgment and very little software vocabulary. They are not slow. They are not fragile. They have simply never been taught the words, and every product they've tried assumed they had been. Our job is to remove the vocabulary requirement, never to lower the ceiling on what they can accomplish.

**The one-line thesis:** the user brings the idea, the taste, and the details only they know. The software brings everything else.

---

## The twelve rules

**1. One question per screen.** If a screen asks two things, it's two screens.

**2. One primary action per screen.** Exactly one button is the obvious next move. Everything else is visibly secondary.

**3. No unexplained words.** Every term outside ordinary English gets defined in visible text the first time it appears. Not a tooltip. Not a hover. Visible.

**4. Text starts at 18px.** Body text 18px minimum, primary text larger. Contrast meets WCAG AA (4.5:1) at every size. Nothing important is dim.

**5. Nothing is hidden behind hover.** Hover doesn't exist on touch and isn't discoverable anywhere. Help is on the page or it isn't help.

**6. Nothing requires drag.** Drag may exist as a shortcut; a button must always do the same job.

**7. Tap targets are at least 44×44 pixels,** with generous space between them.

**8. Always show where you are.** "Step 2 of 4." Always.

**9. Every action can be undone,** and the undo is visible before the action is taken.

**10. Say what happens next.** No screen ends without telling the user what to do with what they just made. If the next step happens outside our software, we show that step literally, with pictures.

**11. Reassure, explicitly.** "You can't break anything here." Fear of breaking things is the single largest brake on this user, and it's cheap to release.

**12. Do the mechanical work.** If the software can do it, the software does it. The user supplies only what they alone know: the idea, the words, the music, the intent.

---

## The Earl Rubric

Applied by the reviewer (Earl, 68, composite of the target demographic) at three gates per program: wireframe, first build, pre-ship. Nothing ships with an open FAIL.

Every screen is read aloud and scored:

| # | Check | Pass condition |
|---|---|---|
| 1 | **Five-second test** | Earl can say aloud what to do next within five seconds of seeing the screen |
| 2 | **Vocabulary** | Zero words Earl can't define, or every such word is defined in visible text on the same screen |
| 3 | **Single action** | Earl points at exactly one button when asked "what would you press?" |
| 4 | **Legibility** | Earl reads every word without leaning in or reaching for glasses |
| 5 | **No dead ends** | Earl knows what happens after he presses the button, before he presses it |
| 6 | **The cliff test** | If the next step is outside our software, Earl can complete it from what we showed him — no outside help |
| 7 | **Fear check** | Earl says he is not worried about breaking something |
| 8 | **Recovery** | Earl can get back to where he was after a wrong turn, without starting over |
| 9 | **Motor check** | Every action is completable with one imprecise click; nothing needs drag or fine positioning |
| 10 | **Dignity check** | Nothing on the screen talks down to Earl, and nothing implies he should already know something |

Rules 1–9 are checkable by a linter for the mechanical portion (type size, contrast, focus, tap targets, color-only signaling, reduced motion). Rule 10 and the read-aloud portions are human judgment and stay that way.

---

## Standing note on the name

"BoomerEZ" is warm to some of this demographic and condescending to others. Rule 10 applies to the product name itself. Make it question one in the first real-user test, and be willing to hear the answer.
