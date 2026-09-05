#!/usr/bin/env python3
"""earl-lint: static rubric linter for BoomerEZ HTML artifacts.

Implements the machine-checkable slice of docs/EARL_RUBRIC.md — baseline
document structure (the mechanical portions of checks 2 and 3), the static
end of check 4 (legibility: font sizes below the 18px floor), the static
end of check 9 (motor: drag interactions, tap-target minimums), plus the
reduced-motion and focus-visibility supports from the design standard.
Contrast ratios, rendered tap-target geometry, and color-only signaling
need a rendering engine; they land with the browser-based audit
(toolchain backlog item 7).

Warn first, fail later: every finding is a warning and the exit code is 0
unless --strict is passed. Reads app HTML only — never edits it
(docs/AGENT_LANES.md).

Usage:
    python3 packages/earl-lint/earl_lint.py [--json OUT] [--strict] PATH [...]

PATH may be an HTML file or a directory (searched recursively for *.html,
skipping dist/ and node_modules/). Exit codes: 0 = clean, or findings
without --strict; 1 = findings with --strict; 2 = usage/config problem.
Stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RUBRIC_PATH = Path(__file__).parent / "rubric.json"
SKIP_DIRS = {"dist", "node_modules", ".git"}
FONT_FLOOR_PX = 18.0
TAP_MIN_PX = 44.0


class DocumentFacts(HTMLParser):
    """Collects the facts rubric checks assert against."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.has_doctype = False
        self.html_lang = None
        self.title_text = ""
        self._in_title = False
        self._in_style = False
        self.has_viewport_meta = False
        self.imgs_missing_alt = 0
        self.css = ""            # every <style> block, concatenated
        self.inline_styles = []  # style="..." attribute values
        self.has_interactive = False
        self.has_draggable_attr = False

    def handle_decl(self, decl: str) -> None:
        if decl.lower().startswith("doctype html"):
            self.has_doctype = True

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attrs_d = dict(attrs)
        if tag == "html":
            self.html_lang = attrs_d.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "style":
            self._in_style = True
        elif tag == "meta" and (attrs_d.get("name") or "").lower() == "viewport":
            self.has_viewport_meta = True
        elif tag == "img" and not (attrs_d.get("alt") or "").strip():
            self.imgs_missing_alt += 1
        if tag in ("a", "button", "input", "select", "textarea", "summary"):
            self.has_interactive = True
        if "draggable" in attrs_d:
            self.has_draggable_attr = True
        if "style" in attrs_d and attrs_d["style"]:
            self.inline_styles.append(attrs_d["style"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text += data
        elif self._in_style:
            self.css += data + "\n"


def _all_css(facts: DocumentFacts) -> str:
    return facts.css + "\n" + "\n".join(facts.inline_styles)


def _px_font_sizes(css: str) -> list:
    return [float(m) for m in re.findall(r"font-size\s*:\s*([\d.]+)\s*px", css)]


def check_doctype(facts, src):
    if not facts.has_doctype:
        return "no <!doctype html> declaration"


def check_html_lang(facts, src):
    if not (facts.html_lang or "").strip():
        return "<html> has no lang attribute"


def check_title(facts, src):
    if not facts.title_text.strip():
        return "document has no non-empty <title>"


def check_viewport(facts, src):
    if not facts.has_viewport_meta:
        return "no viewport meta tag"


def check_img_alt(facts, src):
    if facts.imgs_missing_alt:
        return f"{facts.imgs_missing_alt} <img> element(s) without alt text"


def check_font_floor(facts, src):
    sizes = _px_font_sizes(_all_css(facts))
    below = [s for s in sizes if s < FONT_FLOOR_PX]
    if below:
        return (f"{len(below)} font-size declaration(s) below the "
                f"{FONT_FLOOR_PX:g}px floor (smallest: {min(below):g}px)")


def check_tap_min(facts, src):
    if not facts.has_interactive:
        return None
    mins = [float(m) for m in
            re.findall(r"min-(?:height|width)\s*:\s*([\d.]+)\s*px", _all_css(facts))]
    if not any(m >= TAP_MIN_PX for m in mins):
        return (f"no min-height/min-width of {TAP_MIN_PX:g}px or more declared — "
                "tap targets may be too small for an imprecise click")


def check_drag(facts, src):
    if facts.has_draggable_attr or re.search(r"\bSortable\b", src):
        return ("drag interaction present — confirm every action also "
                "completes with a single click (Earl 9: no drag required)")


def check_reduced_motion(facts, src):
    css = _all_css(facts)
    if re.search(r"\b(transition|animation)\s*:", css) and \
            "prefers-reduced-motion" not in css:
        return "transitions/animations without a prefers-reduced-motion block"


def check_focus_visible(facts, src):
    if facts.has_interactive and ":focus" not in facts.css:
        return "interactive elements but no :focus styling in the stylesheet"


CHECKS = {
    "doctype": check_doctype,
    "html-lang": check_html_lang,
    "title-nonempty": check_title,
    "viewport-meta": check_viewport,
    "img-alt": check_img_alt,
    "font-floor": check_font_floor,
    "tap-min": check_tap_min,
    "drag-path": check_drag,
    "reduced-motion": check_reduced_motion,
    "focus-visible": check_focus_visible,
}


def load_rubric() -> list:
    rubric = json.loads(RUBRIC_PATH.read_text(encoding="utf-8"))
    rules = rubric["rules"]
    for rule in rules:
        if rule["check"] not in CHECKS:
            sys.exit(f"earl-lint: rubric rule {rule['id']} references "
                     f"unknown check {rule['check']!r}")
    return rules


def lint_file(path: Path, rules: list) -> list:
    src = path.read_text(encoding="utf-8", errors="replace")
    facts = DocumentFacts()
    facts.feed(src)
    facts.close()
    findings = []
    for rule in rules:
        detail = CHECKS[rule["check"]](facts, src)
        if detail:
            findings.append({
                "file": str(path),
                "rule": rule["id"],
                "check": rule["check"],
                "earl": rule["earl"],
                "severity": rule["severity"],
                "detail": detail,
            })
    return findings


def collect_html(args: list) -> list:
    files = []
    for arg in args:
        p = Path(arg)
        if p.is_dir():
            files.extend(f for f in sorted(p.rglob("*.html"))
                         if not (SKIP_DIRS & set(part for part in f.parts)))
        elif p.is_file():
            files.append(p)
        else:
            sys.exit(f"earl-lint: no such file or directory: {arg}")
    return files


def render_table(findings: list) -> str:
    headers = ("File", "Rule", "Earl", "Finding")
    rows = [(f["file"], f["rule"], str(f["earl"]), f["detail"]) for f in findings]
    widths = [max(len(headers[i]), *(len(r[i]) for r in rows)) for i in range(4)]
    def fmt(row):
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip()
    lines = [fmt(headers), fmt(tuple("-" * w for w in widths))]
    lines += [fmt(r) for r in rows]
    return "\n".join(lines)


def main(argv: list) -> int:
    strict = "--strict" in argv
    argv = [a for a in argv if a != "--strict"]
    json_out = None
    if "--json" in argv:
        i = argv.index("--json")
        try:
            json_out = Path(argv[i + 1])
        except IndexError:
            sys.exit("earl-lint: --json requires a path")
        del argv[i:i + 2]
    if not argv:
        print(__doc__)
        return 2

    rules = load_rubric()
    files = collect_html(argv)
    if not files:
        print("earl-lint: no HTML files found; nothing to lint.")
        return 0

    findings = []
    for path in files:
        findings.extend(lint_file(path, rules))

    if json_out:
        json_out.write_text(json.dumps(
            {"files": len(files), "findings": findings}, indent=2) + "\n",
            encoding="utf-8")

    if findings:
        print(render_table(findings))
        print(f"\nearl-lint: {len(findings)} warning(s) across {len(files)} "
              f"file(s). Policy is warn-first (docs/AGENT_LANES.md item 4)"
              + (" — failing due to --strict." if strict else "."))
        return 1 if strict else 0
    print(f"earl-lint: {len(files)} file(s) clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
