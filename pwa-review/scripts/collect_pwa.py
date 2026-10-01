#!/usr/bin/env python3
"""Fetch PWA evidence for any agent. No third-party deps.

Usage:
  python3 scripts/collect_pwa.py https://example.com --out /tmp/pwa-evidence.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

UA = "pwa-review/1.0 (+agent-neutral; evidence collector)"
TIMEOUT = 20


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict] = []
        self.metas: list[dict] = []
        self.scripts: list[str] = []
        self._script: list[str] | None = None
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag == "link":
            self.links.append(ad)
        elif tag == "meta":
            self.metas.append(ad)
        elif tag == "script":
            self._script = []
            if ad.get("src"):
                self.scripts.append(f"SRC:{ad['src']}")
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script is not None:
            self.scripts.append("".join(self._script))
            self._script = None
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._script is not None:
            self._script.append(data)
        if self._in_title:
            self.title += data


def fetch(url: str) -> dict:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read(1_500_000)
            return {
                "url": resp.geturl(),
                "status": getattr(resp, "status", 200),
                "content_type": resp.headers.get("content-type", ""),
                "body": raw.decode("utf-8", errors="replace"),
                "error": None,
            }
    except HTTPError as exc:
        body = exc.read(200_000).decode("utf-8", errors="replace")
        return {"url": url, "status": exc.code, "content_type": "", "body": body, "error": f"HTTP {exc.code}"}
    except URLError as exc:
        return {"url": url, "status": 0, "content_type": "", "body": "", "error": str(exc.reason)}


def meta_get(metas: list[dict], name: str) -> str:
    key = name.lower()
    for m in metas:
        if m.get("name", "").lower() == key or m.get("property", "").lower() == key or m.get("http-equiv", "").lower() == key:
            return m.get("content", "")
    return ""


def find_manifest(links: list[dict], base: str) -> str:
    for link in links:
        if link.get("rel", "").lower().split() and "manifest" in link.get("rel", "").lower().split():
            href = link.get("href", "")
            if href:
                return urljoin(base, href)
    return ""


def find_sw(blobs: list[str], base: str) -> str:
    pat = re.compile(r"""navigator\.serviceWorker\.register\(\s*['"]([^'"]+)['"]""")
    for blob in blobs:
        m = pat.search(blob)
        if m:
            return urljoin(base, m.group(1))
    return ""


def flags(text: str) -> dict:
    t = text or ""
    return {
        "install_listener": bool(re.search(r"addEventListener\(\s*['\"]install['\"]|self\.oninstall", t)),
        "activate_listener": bool(re.search(r"addEventListener\(\s*['\"]activate['\"]|self\.onactivate", t)),
        "fetch_listener": bool(re.search(r"addEventListener\(\s*['\"]fetch['\"]|self\.onfetch", t)),
        "cache_api": "caches.open" in t or "cache.put" in t or "caches.match" in t,
        "cache_name": bool(re.search(r"CACHE_NAME|CACHE_VERSION|cacheName", t)),
        "cache_cleanup": "caches.delete" in t or "caches.keys" in t,
        "sync": bool(re.search(r"addEventListener\(\s*['\"]sync['\"]|periodicsync", t)),
        "workbox": "workbox" in t.lower(),
        "skip_waiting": "skipWaiting" in t,
        "clients_claim": "clients.claim" in t,
        "navigation_preload": "navigationPreload" in t,
        "push": bool(re.search(r"addEventListener\(\s*['\"]push['\"]", t)),
        "notificationclick": "notificationclick" in t,
        "message": bool(re.search(r"addEventListener\(\s*['\"]message['\"]", t)),
        "offline_fallback": bool(re.search(r"offline\.(html|htm)", t, re.I)),
        "expiration": "maxEntries" in t or "maxAgeSeconds" in t or "ExpirationPlugin" in t,
    }


def manifest_summary(body: str) -> dict:
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        return {"valid_json": False, "error": str(exc)}
    icons = data.get("icons") or []
    sizes = {str(i.get("sizes", "")) for i in icons if isinstance(i, dict)}
    purposes = " ".join(str(i.get("purpose", "")) for i in icons if isinstance(i, dict))
    return {
        "valid_json": True,
        "name": bool(data.get("name")),
        "short_name": data.get("short_name") or "",
        "has_192": any("192x192" in s for s in sizes),
        "has_512": any("512x512" in s for s in sizes),
        "start_url": bool(data.get("start_url")),
        "display": data.get("display") or "",
        "background_color": bool(data.get("background_color")),
        "theme_color": bool(data.get("theme_color")),
        "description": bool(data.get("description")),
        "screenshots": len(data.get("screenshots") or []),
        "shortcuts": len(data.get("shortcuts") or []),
        "categories": bool(data.get("categories")),
        "orientation": bool(data.get("orientation")),
        "lang_or_dir": bool(data.get("lang") or data.get("dir")),
        "id": bool(data.get("id")),
        "scope": bool(data.get("scope")),
        "maskable": "maskable" in purposes,
        "note_taking": bool(data.get("note_taking")),
        "widgets": bool(data.get("widgets")),
        "handle_links": data.get("handle_links"),
        "launch_handler": bool(data.get("launch_handler")),
        "file_handlers": bool(data.get("file_handlers")),
        "protocol_handlers": bool(data.get("protocol_handlers")),
        "share_target": bool(data.get("share_target")),
        "scope_extensions": bool(data.get("scope_extensions")),
        "icons": len(icons),
    }


def collect(url: str) -> dict:
    page = fetch(url)
    parser = HeadParser()
    if page["body"]:
        parser.feed(page["body"])
    base = page["url"] or url
    manifest_url = find_manifest(parser.links, base)
    sw_url = find_sw(parser.scripts, base)
    probes = []
    origin = f"{urlparse(base).scheme}://{urlparse(base).netloc}"
    if not manifest_url:
        for path in ("/manifest.webmanifest", "/manifest.json"):
            probe = fetch(origin + path)
            probes.append({"url": origin + path, "status": probe["status"], "error": probe["error"]})
            if probe["status"] == 200 and "json" in probe["content_type"] or (probe["status"] == 200 and probe["body"].lstrip().startswith("{")):
                manifest_url = origin + path
                break
    if not sw_url:
        for path in ("/sw.js", "/service-worker.js"):
            probe = fetch(origin + path)
            probes.append({"url": origin + path, "status": probe["status"], "error": probe["error"]})
            if probe["status"] == 200 and "javascript" in probe["content_type"]:
                sw_url = origin + path
                break
    manifest = fetch(manifest_url) if manifest_url else {"url": "", "status": 0, "body": "", "error": "not found", "content_type": ""}
    sw = fetch(sw_url) if sw_url else {"url": "", "status": 0, "body": "", "error": "not found", "content_type": ""}
    apple_splash = [l.get("href", "") for l in parser.links if "apple-touch-startup-image" in l.get("rel", "")]
    apple_icon = [l.get("href", "") for l in parser.links if "apple-touch-icon" in l.get("rel", "")]
    viewport = meta_get(parser.metas, "viewport")
    return {
        "input_url": url,
        "final_url": base,
        "title": parser.title.strip(),
        "page_status": page["status"],
        "page_error": page["error"],
        "https": base.startswith("https://"),
        "manifest_url": manifest_url,
        "manifest_status": manifest["status"],
        "manifest_error": manifest["error"],
        "manifest": manifest_summary(manifest["body"]) if manifest["body"] else {"valid_json": False, "error": manifest["error"]},
        "service_worker_url": sw_url,
        "service_worker_status": sw["status"],
        "service_worker_error": sw["error"],
        "service_worker_flags": flags(sw["body"]),
        "meta": {
            "theme_color": meta_get(parser.metas, "theme-color"),
            "viewport": viewport,
            "viewport_fit_cover": "viewport-fit=cover" in viewport,
            "apple_mobile_web_app_capable": meta_get(parser.metas, "apple-mobile-web-app-capable"),
            "apple_status_bar": meta_get(parser.metas, "apple-mobile-web-app-status-bar-style"),
            "mobile_web_app_capable": meta_get(parser.metas, "mobile-web-app-capable"),
            "csp": meta_get(parser.metas, "content-security-policy"),
            "description": meta_get(parser.metas, "description"),
            "canonical": next((l.get("href", "") for l in parser.links if l.get("rel", "").lower() == "canonical"), ""),
        },
        "apple_touch_icon_count": len(apple_icon),
        "apple_splash_count": len(apple_splash),
        "html_flags": flags("\n".join(parser.scripts) + "\n" + page["body"][:200000]),
        "probes": probes,
        "note": "Evidence only. Score with references/checklist.md. Bundled JS not executed.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Collect PWA audit evidence")
    ap.add_argument("url")
    ap.add_argument("--out", help="Write JSON evidence to this path")
    args = ap.parse_args()
    if not args.url.startswith("http"):
        print("URL must start with http:// or https://", file=sys.stderr)
        return 2
    evidence = collect(args.url)
    text = json.dumps(evidence, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
