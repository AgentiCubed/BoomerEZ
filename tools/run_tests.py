#!/usr/bin/env python3
"""BoomerEZ toolchain test suite — run by CI and locally.

Network-free: checks repo structure, token integrity, the earl-lint rubric,
.gitignore coverage, and the bundler's verification logic against fixtures,
then runs earl-lint (warn-first, read-only) over the real pages. Exits
non-zero on any failure. Stdlib only.

Usage: python3 tools/run_tests.py
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAILURES: list = []


def check(label: str, ok: bool, detail: str = "") -> None:
    print(f"  {'ok' if ok else 'FAIL'}  {label}"
          + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        FAILURES.append(label)


def test_structure() -> None:
    print("Repo structure:")
    for rel in [
        "index.html",
        "apps/mode-studio/index.html",
        "docs/DESIGN_STANDARD.md",
        "docs/EARL_RUBRIC.md",
        "docs/ROADMAP.md",
        "docs/AGENT_LANES.md",
        "docs/DEVLOG.md",
        "packages/tokens/boomerez.css",
        "packages/earl-lint/earl_lint.py",
        "packages/earl-lint/rubric.json",
        "tools/build.py",
        ".github/workflows/ci.yml",
        "README.md",
        "LICENSE",
        ".gitignore",
    ]:
        check(rel, (ROOT / rel).exists(), "missing")


def test_tokens() -> None:
    print("Design tokens:")
    css = (ROOT / "packages/tokens/boomerez.css").read_text(encoding="utf-8")
    props = re.findall(r"--bz-[\w-]+\s*:", css)
    check("boomerez.css defines :root block", ":root" in css)
    check("at least 20 --bz- custom properties", len(props) >= 20,
          f"only {len(props)}")
    check("codifies the shipped ground color #0b0e12", "#0b0e12" in css)
    check("18px type floor token", "--bz-text-floor: 18px" in css)
    check("44px tap-target token", "--bz-tap-min: 44px" in css)
    check("focus-ring token", "--bz-focus-ring" in css)
    check("reduced-motion block", "prefers-reduced-motion" in css)
    check("braces balanced", css.count("{") == css.count("}"))


def test_rubric() -> None:
    print("earl-lint rubric:")
    rubric = json.loads(
        (ROOT / "packages/earl-lint/rubric.json").read_text(encoding="utf-8"))
    check("policy is warn-first", rubric.get("policy") == "warn-first")
    rules = rubric.get("rules", [])
    check("rubric has rules", len(rules) > 0)
    check("rules have id/check/earl/severity/description",
          all({"id", "check", "earl", "severity", "description"} <= set(r)
              for r in rules))
    check("severities valid",
          all(r.get("severity") in ("warn", "error") for r in rules))


def test_gitignore() -> None:
    print(".gitignore coverage:")
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    lines = {ln.strip() for ln in text.splitlines()}
    check("ignores /dist/", "/dist/" in lines or "dist/" in lines)
    check("ignores node_modules", "node_modules/" in lines)
    check("ignores .env", ".env" in lines)
    check("ignores audio", "*.mp3" in lines and "*.wav" in lines)
    check("ignores video/session recordings",
          "*.mp4" in lines and "*.mov" in lines)


def test_devlog() -> None:
    print("Dev log:")
    devlog = (ROOT / "docs/DEVLOG.md").read_text(encoding="utf-8")
    check("DEVLOG has a dated entry (## YYYY-MM-DD)",
          bool(re.search(r"^## \d{4}-\d{2}-\d{2}", devlog, re.MULTILINE)))


def _load_build_module():
    spec = importlib.util.spec_from_file_location("bz_build", ROOT / "tools/build.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bundler_logic() -> None:
    print("Bundler verification logic (fixtures, no network):")
    build = _load_build_module()
    check("SHA-256 pin is 64 hex chars",
          bool(re.fullmatch(r"[0-9a-f]{64}", build.SORTABLE_SHA256)))
    dirty = ('<link href="https://fonts.googleapis.com/css2?x" rel="stylesheet">'
             '<script src="https://cdn.example.com/lib.js"></script>'
             '<div style="background:url(https://cdn.example.com/bg.png)"></div>')
    clean = ('<script>inline()</script><style>@font-face{src:url(data:font/woff2;'
             'base64,AA==)}</style><a href="https://example.com">a link</a>')
    check("flags external script/link/css url()",
          len(build.find_externals(dirty)) == 3,
          f"found {len(build.find_externals(dirty))}, expected 3")
    check("passes inlined page (plain <a> links allowed)",
          build.find_externals(clean) == [])


def test_earl_lint_runs() -> None:
    print("earl-lint execution (warn-first, read-only):")
    result = subprocess.run(
        [sys.executable, str(ROOT / "packages/earl-lint/earl_lint.py"),
         str(ROOT / "index.html"), str(ROOT / "apps")],
        capture_output=True, text=True)
    detail = (result.stdout + result.stderr).strip().replace("\n", " | ")[-300:]
    check("earl-lint exits 0 over the real pages", result.returncode == 0, detail)


def main() -> int:
    for test in (test_structure, test_tokens, test_rubric, test_gitignore,
                 test_devlog, test_bundler_logic, test_earl_lint_runs):
        test()
    if FAILURES:
        print(f"\n{len(FAILURES)} test failure(s).")
        return 1
    print("\nAll tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
