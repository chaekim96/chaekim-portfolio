#!/bin/sh
# Renders scripts/og.html (the link-preview card: 김 tile, name, one-liner) to
# assets/img/og-card.png at 1200x630, and copies it over the legacy og.png.
# Pages reference og-card.png; rename it again if a redesign needs to beat share caches.
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$(mktemp -d)/og@2x.png"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1200,630 --screenshot="$OUT" --virtual-time-budget=6000 \
  "file://$DIR/scripts/og.html" >/dev/null 2>&1
sips -z 630 1200 -s format png "$OUT" --out "$DIR/assets/img/og-card.png" >/dev/null
cp "$DIR/assets/img/og-card.png" "$DIR/assets/img/og.png"
echo "wrote assets/img/og-card.png (+ og.png)"
