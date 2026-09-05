#!/usr/bin/env python3
"""Offline bundler for BoomerEZ — toolchain backlog item 2 (docs/AGENT_LANES.md).

Copies the landing page and every app into dist/, inlines the pinned
third-party assets so each page works with zero network access, then verifies
that no external resource requests remain — and exits non-zero if any do.
CI runs this, so a stray external reference fails the build.

Inlining:
- Pinned vendor scripts (Sortable 1.15.2) are downloaded, SHA-256-verified
  against the pin below, and inlined into their <script> tags. A hash
  mismatch aborts the build; re-pin only after verifying the file by hand.
- Google Fonts stylesheet links become embedded @font-face rules carrying
  base64 woff2 data (latin subset), so the font ships inside the page.

Sources are read, never edited (docs/AGENT_LANES.md) — all rewriting happens
on the dist/ copies.

Offline/local runs: set BOOMEREZ_VENDOR_DIR to a directory holding
Sortable.min.js, fonts.css, and the woff2 files fonts.css references
(named by their URL basename); hash verification still applies.

Usage: python3 tools/build.py
Stdlib only.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# Pin computed 2026-09-05 from the npm dist file
# (registry.npmjs.org/sortablejs/-/sortablejs-1.15.2.tgz :: package/Sortable.min.js),
# which cdnjs and jsdelivr mirror byte-for-byte. If a CDN ever serves
# different bytes, the build aborts loudly — verify by hand before re-pinning.
SORTABLE_SHA256 = "ca68430703c4f5960e90735867c6e94d29b5a3de37107d8100e5a301007e9e6e"
SORTABLE_URLS = [
    "https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.2/Sortable.min.js",
    "https://cdn.jsdelivr.net/npm/sortablejs@1.15.2/Sortable.min.js",
]

FONT_SUBSET = "latin"
# Chrome-like UA so fonts.googleapis.com serves woff2 sources.
FONT_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

EXCLUDE_NAMES = {".gitkeep", ".DS_Store"}
EXCLUDE_DIRS = {"sample-library", "user-files"}


def _vendor_path(url: str) -> Path | None:
    vendor_dir = os.environ.get("BOOMEREZ_VENDOR_DIR")
    if not vendor_dir:
        return None
    name = "fonts.css" if "/css2" in url else Path(urlparse(url).path).name
    return Path(vendor_dir) / name


def fetch(url: str) -> bytes:
    local = _vendor_path(url)
    if local is not None:
        return local.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": FONT_UA})
    last_err = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except Exception as err:  # noqa: BLE001 — retried, then re-raised
            last_err = err
    raise RuntimeError(f"failed to fetch {url}: {last_err}")


def fetch_sortable() -> str:
    last_err = None
    for url in SORTABLE_URLS:
        try:
            data = fetch(url)
        except Exception as err:  # noqa: BLE001
            last_err = err
            continue
        digest = hashlib.sha256(data).hexdigest()
        if digest != SORTABLE_SHA256:
            sys.exit(f"build: SHA-256 mismatch for {url}\n"
                     f"  expected {SORTABLE_SHA256}\n"
                     f"  got      {digest}\n"
                     "Refusing to inline unverified vendor code.")
        return data.decode("utf-8")
    sys.exit(f"build: could not fetch Sortable from any pinned URL: {last_err}")


def inline_scripts(html: str, sortable_js: list) -> str:
    """Replace pinned external <script src> tags with inline, verified code.

    sortable_js is a single-element list used as a lazy cache so the download
    happens only when a page actually references the library.
    """
    def repl(match: re.Match) -> str:
        url = match.group(1)
        if url in SORTABLE_URLS:
            if not sortable_js:
                sortable_js.append(fetch_sortable())
            return ("<script>/* Sortable 1.15.2 — inlined by tools/build.py, "
                    f"sha256 {SORTABLE_SHA256[:16]}… */\n"
                    + sortable_js[0] + "</script>")
        return match.group(0)  # unknown external: left for verify to flag

    return re.sub(
        r'<script\s+src=["\'](https?://[^"\']+)["\'][^>]*>\s*</script>',
        repl, html)


def _font_faces(css: str) -> str:
    """Keep only the FONT_SUBSET @font-face blocks, woff2 URLs inlined."""
    out = []
    for match in re.finditer(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})",
                             css):
        subset, block = match.group(1), match.group(2)
        if subset != FONT_SUBSET:
            continue
        for url in re.findall(r"url\((https?://[^)]+)\)", block):
            data = base64.b64encode(fetch(url)).decode("ascii")
            block = block.replace(url, f"data:font/woff2;base64,{data}")
        out.append(block)
    return "\n".join(out)


def inline_fonts(html: str) -> str:
    def repl(match: re.Match) -> str:
        css = fetch(match.group(1)).decode("utf-8")
        faces = _font_faces(css)
        if not faces:
            sys.exit("build: Google Fonts stylesheet yielded no "
                     f"'{FONT_SUBSET}' @font-face blocks — cannot inline.")
        return ("<style>/* fonts inlined by tools/build.py "
                f"({FONT_SUBSET} subset) */\n" + faces + "\n</style>")

    html = re.sub(
        r'<link[^>]+href=["\'](https?://fonts\.googleapis\.com/css2[^"\']+)["\'][^>]*>',
        repl, html)
    # Preconnect hints to font hosts are pointless offline — drop them.
    return re.sub(
        r'<link[^>]+rel=["\']preconnect["\'][^>]+fonts\.g[^>]*>\s*', "", html)


EXTERNAL_PATTERNS = [
    ("script src", re.compile(r'<script[^>]+src\s*=\s*["\']https?://[^"\']+', re.I)),
    ("link href", re.compile(r'<link[^>]+href\s*=\s*["\']https?://[^"\']+', re.I)),
    ("media src", re.compile(
        r'<(?:img|source|iframe|embed|audio|video)[^>]+src\s*=\s*["\']https?://[^"\']+',
        re.I)),
    ("css url()", re.compile(r'url\(\s*["\']?https?://', re.I)),
    ("css @import", re.compile(r'@import\s+["\']?https?://', re.I)),
]


def find_externals(html: str) -> list:
    """Return residual external *resource* requests (plain <a> links are fine)."""
    found = []
    for label, pattern in EXTERNAL_PATTERNS:
        for match in pattern.finditer(html):
            snippet = match.group(0)[:100]
            found.append(f"{label}: {snippet}")
    return found


def collect_sources() -> list:
    sources = []
    landing = ROOT / "index.html"
    if landing.is_file():
        sources.append(landing)
    apps = ROOT / "apps"
    if apps.is_dir():
        for src in sorted(apps.rglob("*")):
            if not src.is_file() or src.name in EXCLUDE_NAMES:
                continue
            if EXCLUDE_DIRS & set(src.relative_to(apps).parts):
                continue
            sources.append(src)
    return sources


def main() -> int:
    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()

    sortable_cache: list = []
    manifest_files = []
    problems = []

    for src in collect_sources():
        rel = src.relative_to(ROOT)
        dest = DIST / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix == ".html":
            html = src.read_text(encoding="utf-8")
            html = inline_scripts(html, sortable_cache)
            html = inline_fonts(html)
            dest.write_text(html, encoding="utf-8")
            for issue in find_externals(html):
                problems.append(f"{rel}: {issue}")
        else:
            shutil.copy2(src, dest)
        manifest_files.append({"file": str(rel), "bytes": dest.stat().st_size})

    (DIST / "build-manifest.json").write_text(json.dumps({
        "files": manifest_files,
        "vendored": {
            "sortablejs": {"version": "1.15.2", "sha256": SORTABLE_SHA256,
                           "inlined": bool(sortable_cache)},
            "fonts": {"family": "JetBrains Mono", "subset": FONT_SUBSET},
        },
    }, indent=2) + "\n", encoding="utf-8")

    for entry in manifest_files:
        print(f"  {entry['file']}  ({entry['bytes']:,} bytes)")

    if problems:
        print("\nbuild: external resource requests remain after inlining:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print(f"\nbuild: {len(manifest_files)} file(s) in dist/, "
          "zero external resource requests.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
