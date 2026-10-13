---
name: site-shots
description: Screenshot the site in all six theme combinations (Professional/Village/Terminal × light/dark) with real content loaded. Use after any visual or layout change to index.html, before telling the user it looks right.
---

# Site screenshots

Run `bash .claude/skills/site-shots/shots.sh [out-dir] [width]`, then read the PNGs it lists.

- Default width is 1680. Also check `1260`, the narrowest width where the fixed side rails show, so content must clear them.
- Headless Chrome won't render narrower than ~500px. To check phone width, load the page in a 390px `<iframe>` inside a wrapper page and screenshot that.
- The script serves a temp copy over HTTP, because `data.json` doesn't load from `file://`.
- It writes outside the repo by default. Never commit screenshots.
