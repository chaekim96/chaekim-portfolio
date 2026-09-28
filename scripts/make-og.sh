#!/bin/sh
# Renders scripts/og.html to assets/img/og.png (1200x630, shot at 2x then downsized).
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$(mktemp -d)/og@2x.png"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1200,630 --screenshot="$OUT" --virtual-time-budget=6000 \
  "file://$DIR/scripts/og.html" >/dev/null 2>&1
sips -z 630 1200 -s format png "$OUT" --out "$DIR/assets/img/og.png" >/dev/null
echo "wrote assets/img/og.png"
