# thayagapriyan.github.io

Personal site, published at <https://thayagapriyan.github.io>.
Plain HTML, CSS and JavaScript — no build step, no dependencies.

## Editing content

**Almost everything you'll want to change lives in `data.json`.**
Open it, change the text, save, commit. No HTML involved.

| To change | Edit in `data.json` |
|---|---|
| Job titles, dates, descriptions | `experience` |
| Projects shown under Selected Work | `work` |
| Skill groups and tags | `stack` |

Three rules for `data.json`:

- It's JSON, so keep the quotes and commas. A missing comma means nothing
  renders. Paste the file into <https://jsonlint.com> if the page goes blank.
- In `stack`, a trailing `*` marks a skill as primary — it renders brighter.
  `"Java*"` is emphasised, `"Groovy"` is not.
- In `experience` and `work`, the description fields allow `<strong>` for
  emphasis. Everything else is escaped.

### Themes

Two independent controls:

- **Palette** — the switcher in the left gutter: Professional (default),
  Village, Terminal. Stored as `data-palette` on `<html>`.
- **Light or dark** — pull the mule tail at the top right. Stored as
  `data-mode`.

Both persist in `localStorage`. Professional/light is what a first-time
visitor sees. The village illustration and kolam dividers only appear in
the Village palette. To change a palette's colors, edit its block near the
top of the `<style>` in `index.html`.

### What is NOT in data.json

These are in `index.html` directly, because they're one-offs:

- Your name, headline and intro paragraph — near the top, in `<header>`
- The pipeline diagram — search for `<svg` in the `.pipe` block
- All styling — the `<style>` block; colors are the `--variables` at the very top

## Running it locally

The page loads `data.json` with `fetch`, which browsers block when you open
the file directly (`file://`). **Opening index.html by double-clicking will
show an error where the content should be.** Serve it instead:

    python -m http.server 8000

Then visit <http://localhost:8000>. Changes appear on refresh.

## Résumé

`resumes/` holds three formats — see `resumes/README.md` for how to
regenerate the PDF after editing.

## Publishing

Push to `main`. GitHub Pages serves the repo root; `.nojekyll` keeps Jekyll
out of the way.
