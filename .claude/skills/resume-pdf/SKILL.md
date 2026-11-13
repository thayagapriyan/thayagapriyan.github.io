---
name: resume-pdf
description: Regenerate the résumé PDF from resumes/index.html and verify it is exactly one page. Use after any edit to resumes/index.html, or when asked to add, change or trim résumé content.
---

# Résumé PDF

The résumé must stay **exactly one page** in print: experience on the left, skills and achievements in the right sidebar.

1. Edit `resumes/index.html` (not the PDF).
2. Run `bash .claude/skills/resume-pdf/build.sh`. It prints the page count and exits non-zero unless it is 1.
3. If it spills to page 2, see what moved with
   `pdftotext -layout -f 2 -l 2 resumes/*.pdf -` (Git Bash ships `pdftotext`), then trim:
   - Tighten new bullets to ~2 printed lines (~95 chars per line in the experience column).
   - Drop or merge bullets that repeat another bullet.
   - Key Technical Achievements repeats the experience bullets, so trim it before cutting real experience.
   - A blank page 2 means the page is just over full: trim a line, don't add margins.
   - Change the print CSS (`@media print`) only as a last resort, and say so.
4. Tell the user what you cut. Regenerate the ATS `.docx` with `python .claude/skills/resume-pdf/docx.py` (single column, same content).
   Check it is one page by opening it in Word (COM: `Documents.Open(...).ComputeStatistics(2)`); if it spills, the HTML
   trims above usually fix both, otherwise tighten spacing in `docx.py`.

The script finds Chrome on PATH or at the default Windows path; set `CHROME=/path/to/chrome` to override.
