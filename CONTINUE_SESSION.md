# Continuation Prompt — Human Design Wiki

Paste this into a new Claude session to continue work on the wiki.

---

```
I'm continuing work on my Human Design Wiki.

PROJECT LOCATION
- Local repo: ~/Developer/human-design-wiki  (moved off Google Drive on 09.05.26)
- GitHub repo: https://github.com/theshelbyinbox/human-design-wiki
- Live site: https://theshelbyinbox.github.io/human-design-wiki/
- gh CLI is logged in as theshelbyinbox on my Mac (pushes happen from my machine / Desktop Commander)
- Source material (transcripts, books, course files) still lives in Google Drive at
  ➌ Resources/★ Wikipedia/02 Human Design 🧬/🧠 Human Design Brain/
  That folder is for reading FROM. The repo is never kept there.

NEVER PUT THIS REPO IN A SYNCED FOLDER
It lived in Google Drive until 09.05.26 and Drive silently corrupted the git
database three separate ways: it deleted .git/HEAD (git stopped recognising the
folder as a repo at all), it dropped three loose objects including .gitignore's
blob (commits failed with "error: Error building trees"), and it deleted the
zero-byte .nojekyll file that makes GitHub Pages serve content/*.md. Drive,
Dropbox, iCloud and OneDrive all do this. Keep the repo on local disk.

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
