#!/usr/bin/env bash
# Regenerate the résumé PDF from resumes/index.html; fail unless it is exactly 2 pages.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

PDF=resumes/Thayagapriyan_Dravidamani_Integration_Lead_Resume.pdf
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chrome \
  || echo "/c/Program Files/Google/Chrome/Application/chrome.exe")}
PY=$(command -v python || command -v python3)
winpath() { if command -v cygpath >/dev/null; then cygpath -m "$1"; else echo "$1"; fi; }
ROOT=$(winpath "$PWD")

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$ROOT/$PDF" "file:///${ROOT#/}/resumes/index.html" 2>/dev/null

pages=$("$PY" -c "import re,sys;print(len(re.findall(rb'/Type\s*/Page[^s]',open(sys.argv[1],'rb').read())))" "$PDF")
echo "$PDF: $pages page(s)"
[ "$pages" -eq 2 ] || { echo "FAIL: résumé must be exactly 2 pages" >&2; exit 1; }
