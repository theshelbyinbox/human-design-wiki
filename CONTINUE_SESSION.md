# Continuation Prompt — Human Design Wiki

Paste this into a new Claude session to continue work on the wiki.

---

```
I'm continuing work on my Human Design Wiki.

PROJECT LOCATION
- Local repo (Google Drive): ➌ Resources/★ Wikipedia/02 Human Design 🧬/🧠 Human Design Brain/wiki
- GitHub repo: https://github.com/theshelbyinbox/human-design-wiki
- Live site: https://theshelbyinbox.github.io/human-design-wiki/
- gh CLI is logged in as theshelbyinbox on my Mac (pushes happen from my machine / Desktop Commander)

ARCHITECTURE (markdown-first, migrated 08.20.26 — replaces the old single-file SPA)
- content/<section>/<slug>.md = one article per file, YAML frontmatter: title, section, related
- manifest.json = curated sidebar nav + article index + wikilink map (generated, nav order preserved)
- aliases.json = manual wikilink aliases
- search-index.json = generated full-text search
- index.html = shell only (design + routing + renderer). NO content inside. Never paste articles into it.
- build.js = run after any content change: node build.js
  (new articles are NOT auto-added to the sidebar; use --add-nav or edit manifest.json navSections)

TO ADD/EDIT AN ARTICLE
1. Write/edit the .md in content/ (wikilinks: [[Title]] or [[Title|Label]])
2. node build.js
3. Commit + push (from my machine, not a sandbox)

RULES
- The old no-backticks rule is DEAD — content is plain markdown now
- Sidebar nav is curated by hand — never bulk-append articles to it without asking
- The top-level folders (gates/, concepts/, etc.) are legacy source material, not site content
- This wiki was built with the sd-wiki-brain skill — use that skill for standards
```
