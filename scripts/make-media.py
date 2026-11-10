#!/usr/bin/env python3
"""Makes smaller copies of images in headless Chrome, which can encode WebP and MP4 with nothing to install.

Usage:  python3 scripts/make-media.py
  - every JPG or PNG an <img> uses gets a WebP copy beside it, kept only when it is at least 15% smaller
    (build pages then point at it; see prefer_webp in stamp_shared.py)
  - every GIF in VIDEO_GIFS gets an MP4 and a WebP poster, for a <video autoplay muted loop playsinline>
Then run python3 scripts/build.py and commit the new files.
"""
import http.server
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PAGE = Path(__file__).resolve().parent / "media" / "convert.html"
VIDEO_GIFS = ["/assets/img/home-gif/home.gif", "/assets/img/yin-yang/yin-yang.gif",
              "/assets/img/iu-study-assistant/iusa/poster.gif"]


def stills():
    found = set()
    for page in [*ROOT.glob("*.html"), *(ROOT / "projects").glob("*.html")]:
        found |= set(re.findall(r'<img\b[^>]*?\ssrc="(/assets/img/[^"?#]+\.(?:jpe?g|png))"', page.read_text(encoding="utf-8")))
    return sorted(s for s in found if (ROOT / s.lstrip("/")).exists())


def main():
    out = Path(tempfile.mkdtemp())
    todo = [s for s in stills() if not (ROOT / s.lstrip("/")).with_suffix(".webp").exists()]
    gifs = [g for g in VIDEO_GIFS if not (ROOT / g.lstrip("/")).with_suffix(".mp4").exists()]
    if not todo and not gifs:
        return print("nothing to make")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(ROOT), **k)
        def log_message(self, *a):
            pass
        def do_GET(self):
            body = {"/__conv": PAGE.read_bytes(), "/__list": json.dumps(todo).encode(), "/__gifs": json.dumps(gifs).encode()}.get(self.path)
            if body is None:
                return super().do_GET()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)
        def do_POST(self):
            data = self.rfile.read(int(self.headers["content-length"]))
            dst = out / urllib.parse.unquote(self.path.split("/__save/", 1)[1])
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(data)
            self.send_response(204)
            self.end_headers()

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    with tempfile.TemporaryDirectory() as profile:
        chrome = subprocess.Popen([CHROME, "--headless", "--no-first-run", f"--user-data-dir={profile}", "--remote-debugging-port=0",
                                   f"http://127.0.0.1:{server.server_port}/__conv"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        start = time.time()
        while not (out / "_done").exists() and time.time() - start < 600:
            time.sleep(1)
        chrome.terminate()
    server.shutdown()
    print((out / "_done").read_text() if (out / "_done").exists() else "timed out")
    kept = 0
    for made in out.rglob("*"):
        rel = made.relative_to(out)
        if made.is_dir() or rel.name == "_done":
            continue
        if made.suffix == ".webp" and not rel.name.endswith("-poster.webp"):
            original = next(p for p in (ROOT / rel.with_suffix(e) for e in (".jpg", ".jpeg", ".png")) if p.exists())
            if made.stat().st_size > 0.85 * original.stat().st_size:
                continue
        shutil.copy(made, ROOT / rel)
        kept += 1
    print(f"kept {kept} files")


if __name__ == "__main__":
    main()
