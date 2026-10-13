# AGENTS.md

Personal site and résumé for Thayagapriyan Dravidamani, served by GitHub Pages from `main`.
Plain HTML/CSS/JS. No build step, no dependencies, no package.json. Keep it that way.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The whole site: styles, markup, and the script that renders `data.json` |
| `data.json` | Experience, Selected Work and Stack content. The `profile` block is **not rendered**; the header is hard-coded in `index.html` |
| `favicon.svg` | Serif "T" monogram, linked from both pages |
| `resumes/index.html` | Web résumé; source of the PDF. Fonts are inlined as base64, so lines are huge: grep or read by line range |
| `resumes/*.pdf` | Generated from `resumes/index.html`. Never edit directly |
| `resumes/*.docx` | ATS version, maintained by hand in Word. Agents can't update it; tell the user when it falls out of sync |

## Rules

- **Résumé is exactly two pages.** After editing `resumes/index.html`, use the `resume-pdf` skill (`.claude/skills/resume-pdf/`).
- **Résumé files are named** `Thayagapriyan_Dravidamani_Integration_Lead_Resume.{pdf,docx}`. Several pages link to them by name (`index.html`, `data.json`, `resumes/index.html`, `resumes/README.md`). If you rename them, update every link in the same change.
- **Content edits go in `data.json`** where possible. Descriptions allow `<strong>`; everything else is escaped. In `stack`, a trailing `*` marks a primary skill.
- **Themes** are two independent attributes on `<html>`: `data-palette` (`pro` | `village` | `tech`) and `data-mode` (`light` | `dark`). Palettes differ in colour **and** type/shape (Village = Source Serif + pill shapes; Terminal = mono headings, square corners, cursor). Decorative illustrations or diagrams are not wanted; the user removed them.
- **Layout:** at ≥1240px the content fills the space between the fixed side rails (`.shell` padding clears them). Prose is capped (`--prose`, `85ch` on role text) for readability.
- **Visual changes:** check them with the `site-shots` skill before saying they look right.

## Running locally

`python -m http.server 8000` from the repo root. Opening `index.html` directly fails, because `data.json` doesn't load over `file://`.

## Publishing

Push to `main`; Pages serves the repo root. `.nojekyll` disables Jekyll. Commit only when the user asks.
