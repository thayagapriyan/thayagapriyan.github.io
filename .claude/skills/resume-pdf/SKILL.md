---
name: resume-pdf
description: Regenerate the résumé PDF from resumes/index.html and verify it is exactly two pages. Use after any edit to resumes/index.html, or when asked to add, change or trim résumé content.
---

# Résumé PDF

The résumé must stay **exactly two pages** in print.

1. Edit `resumes/index.html` (not the PDF).
2. Run `bash .claude/skills/resume-pdf/build.sh`. It prints the page count and exits non-zero unless it is 2.
3. If it spills to page 3, see what moved with
   `pdftotext -layout -f 3 -l 3 resumes/*.pdf -` (Git Bash ships `pdftotext`), then trim:
   - Tighten new bullets to ~2 printed lines (~120 chars per line).
   - Drop or merge bullets that repeat another bullet.
   - Key Technical Achievements repeats the experience bullets, so trim it before cutting real experience.
   - Change the print CSS (`@media print`) only as a last resort, and say so.
4. Tell the user what you cut. The `.docx` is edited by hand in Word, so remind them it was not updated.

The script finds Chrome on PATH or at the default Windows path; set `CHROME=/path/to/chrome` to override.
