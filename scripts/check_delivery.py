"""Verify deployed HTTP behavior and bytes; use --preview for Vercel protection bypass."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def check(base: str, preview: bool, resolve_ip: str | None = None) -> None:
    manifest = json.loads((ROOT / "site/assets/manifest.json").read_text())
    routes = json.loads((ROOT / "routing-manifest.json").read_text())
    cases = []
    for path, md in routes.items():
        name = "index.html" if path == "/" else path.lstrip("/")
        cases.extend(
            [
                (path, "text/html", name, 200, "text/html"),
                (path, "text/markdown", md.lstrip("/"), 200, "text/markdown"),
            ]
        )
    for path in (
        "robots.txt",
        "llms.txt",
        "sitemap.xml",
        "agents.json",
        "agents/index.json",
        "data-guide.md",
        "agents/stripe-minions.json",
        "agents/stripe-minions.md",
        "notes/stop-a-run.md",
    ):
        mime = (
            "application/json"
            if path.endswith(".json")
            else "text/markdown"
            if path.endswith(".md")
            else "application/xml"
            if path.endswith(".xml")
            else "text/plain"
        )
        cases.append(("/" + path, "*/*", path, 200, mime))
    for hashed in manifest.values():
        cases.append(("/assets/" + hashed, "*/*", "assets/" + hashed, 200, None))
    for path in ("/missing-page", "/missing/nested/page.html", "/agents/does-not-exist.json"):
        cases.append((path, "text/html", "404.html", 404, "text/html"))
    for accept, name, mime in (
        ("*/*", "index.html", "text/html"),
        ("text/markdown;q=0", "index.html", "text/html"),
        ("text/html,text/markdown;q=0.5", "index.html", "text/html"),
        ("text/markdown,text/html;q=0.5", "index.md", "text/markdown"),
    ):
        cases.append(("/?q=stripe", accept, name, 200, mime))

    def verify(case):
        path, accept, name, expected_status, mime = case
        with tempfile.TemporaryDirectory() as folder:
            headers, body = Path(folder) / "headers", Path(folder) / "body"
            curl = [
                "-sS",
                "--max-time",
                "30",
                "-H",
                "Accept: " + accept,
                "-D",
                str(headers),
                "-o",
                str(body),
            ]
            command = (
                ["vercel", "curl", path, "--deployment", base, "--scope", "nen-labs", "--", *curl]
                if preview
                else ["curl", base.rstrip("/") + path, *curl]
            )
            if resolve_ip and not preview:
                command.extend(["--resolve", f"{urlsplit(base).hostname}:443:{resolve_ip}"])
            result = subprocess.run(command, capture_output=True, text=True, timeout=50)
            if result.returncode:
                raise AssertionError(f"Request failed: {path}: {result.stderr}")
            blocks = headers.read_text().strip().split("\n\n")
            lines = blocks[-1].splitlines()
            status = int(lines[0].split()[1])
            values = dict(
                (k.lower(), v.strip())
                for k, v in (line.split(":", 1) for line in lines[1:] if ":" in line)
            )
            assert status == expected_status, f"{path} [{accept}]: HTTP {status}"
            received = body.read_bytes()
            if preview and name.endswith(".html"):
                # Vercel appends its feedback toolbar to protected preview HTML only.
                received = re.sub(
                    rb'<script async data-explicit-opt-in="true" data-deployment-id="[^"]+" src="https://vercel.live/_next-live/feedback/feedback.js"></script>\s*$',
                    b"",
                    received,
                )
            assert received == (ROOT / "site" / name).read_bytes(), (
                f"{path} [{accept}]: body differs from {name}"
            )
            if mime:
                assert values.get("content-type", "").startswith(mime), (
                    f"{path}: wrong Content-Type {values}"
                )
            if path.split("?")[0] in routes:
                assert "accept" in values.get("vary", "").lower(), f"{path}: missing Vary"
                assert "alternate" in values.get("link", ""), f"{path}: missing Link discovery"
            cache = values.get("cache-control", "")
            if path.startswith("/assets/"):
                assert "immutable" in cache and "31536000" in cache, f"{path}: {cache}"
            else:
                assert "must-revalidate" in cache, f"{path}: {cache}"
        return f"{expected_status} {path} [{accept}]"

    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(verify, cases):
            print(result)
    # Alternate the same URL after warming both targets to catch cache contamination.
    for accept, name in (("text/markdown", "index.md"), ("text/html", "index.html")) * 2:
        verify(("/", accept, name, 200, accept))
    print(f"Passed {len(cases) + 4} deployed response checks for {base}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument(
        "--resolve-ip", help="Use a verified public DNS address while local DNS propagates."
    )
    args = parser.parse_args()
    check(args.base, args.preview, args.resolve_ip)
