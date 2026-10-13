#!/usr/bin/env bash
# Screenshot index.html in every palette × mode, with data.json loaded.
# Usage: shots.sh [out-dir] [width]   (defaults: $TMPDIR/site-shots, 1680)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

OUT=${1:-${TMPDIR:-/tmp}/site-shots}; W=${2:-1680}; PORT=8799
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chrome \
  || echo "/c/Program Files/Google/Chrome/Application/chrome.exe")}
PY=$(command -v python || command -v python3)
winpath() { if command -v cygpath >/dev/null; then cygpath -m "$1"; else echo "$1"; fi; }

mkdir -p "$OUT"
cp data.json favicon.svg "$OUT/"
# ponytail: theme is pinned by baking it into a copy; the page has no URL switch for it
for p in pro village tech; do for m in light dark; do
  sed -e "s/<html lang=\"en\">/<html lang=\"en\" data-palette=\"$p\" data-mode=\"$m\">/" \
      -e 's/localStorage.getItem("palette")/null/; s/localStorage.getItem("mode")/null/' \
      index.html > "$OUT/$p-$m.html"
done; done

(cd "$OUT" && exec "$PY" -m http.server "$PORT" >/dev/null 2>&1) & srv=$!
trap 'kill $srv 2>/dev/null' EXIT
sleep 1

for p in pro village tech; do for m in light dark; do
  "$CHROME" --headless --disable-gpu --hide-scrollbars --virtual-time-budget=3000 \
    --window-size="$W,1400" --screenshot="$(winpath "$OUT")/$p-$m.png" \
    "http://localhost:$PORT/$p-$m.html" 2>/dev/null
done; done
ls "$OUT"/*.png
