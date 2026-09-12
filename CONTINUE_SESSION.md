# Continuation Prompt -- Human Design Wiki

Paste this into a new Claude session to continue work on the wiki.

---

```
I'm continuing work on my Human Design Wiki. Session mode: Wiki only.

PROJECT LOCATION
- Local repo: ~/Developer/human-design-wiki  (moved off Google Drive on 09.05.26)
- GitHub repo: https://github.com/theshelbyinbox/human-design-wiki
- Live site: https://theshelbyinbox.github.io/human-design-wiki/
- gh CLI is logged in as theshelbyinbox on my Mac (pushes happen from my machine)
- Source material (transcripts, books, course files) still lives in Google Drive at
  ➌ Resources/★ Wikipedia/02 Human Design 🧬/🧠 Human Design Brain/
  That folder is for reading FROM. The repo is never kept there.
- Connect BOTH folders when a session needs library and repo together. It is far
  faster than reaching the repo through Desktop Commander alone.

NEVER PUT THIS REPO IN A SYNCED FOLDER
It lived in Google Drive until 09.05.26 and Drive silently corrupted the git
database three ways: it deleted .git/HEAD (git stopped recognising the folder as
a repo at all), it dropped three loose objects including .gitignore's blob
(commits failed with "error: Error building trees"), and it deleted the
zero-byte .nojekyll file that makes GitHub Pages serve content/*.md. Drive,
Dropbox, iCloud and OneDrive all do this. Keep the repo on local disk.

ARCHITECTURE (markdown-first, migrated 08.20.26)
- content/<section>/<slug>.md = one article per file, YAML frontmatter: title,
  section, related
- manifest.json = curated sidebar nav + article index + wikilink map (generated,
  nav order preserved)
- aliases.json = manual wikilink aliases. IMPORTANT: aliases WIN over article
  titles in build.js (line 74 runs after line 73), so an alias can silently
  shadow a real article. Check aliases.json before naming anything.
- search-index.json = generated full-text search
- index.html = shell only. NO content inside. Never paste articles into it.
- build.js = run after any content change: node build.js
- Order of operations when adding articles that link to each other:
  write -> node build.js -> verify. Verify reads manifest.json, so new
  cross-links look "bad" until after the build.

TO ADD/EDIT AN ARTICLE
1. Write/edit the .md in content/ (wikilinks: [[Title]] or [[Title|Label]])
2. node build.js
3. python3 tools/hdwiki.py verify content/<section>
4. Commit + push (from my machine, not a sandbox)

RULES
- The old no-backticks rule is DEAD - content is plain markdown now
- No em dashes in prose. The wiki's dash is " -- ". Em dashes INSIDE wikilink
  targets are fine, since some article titles contain them.
- No markdown tables. No emojis in files.
- Sidebar nav is curated by hand - never bulk-append articles to it without asking
- The top-level folders (gates/, concepts/, etc.) are legacy source material,
  not site content
- This wiki was built with the sd-wiki-brain skill - use that skill for standards

STATE AS OF 09.12.26 (second session, cleanup pass)

Whole-wiki cleanup landed. `verify content` went from 344 of 428 files with
problems to 0 of 428. Commit b27df21, pushed, Pages build confirmed, live
content spot-checked. 344 content files changed. Sidebar nav and aliases.json
untouched (nav hash checked before and after build.js).

What the pass did:
- 6,432 em dashes in prose became " -- ". 168 en dashes in transit date ranges
  became "to" (spaced, "June 1 to 7") or a hyphen (unspaced, "Nov 6-11").
- Three tables became flat bullets with inline labels, one bullet per former
  row: inner-authority-overview (seven authorities), mind-vs-body (mind-led vs
  body-led), strategy-and-signature (type / signature / not-self). Flat on
  purpose: index.html's renderMarkdown ignores list indentation, so nested
  bullets render as one level.
- 44 distinct bad wikilink targets rewritten in place with the label kept, so
  the page text reads the same: [[Throat]] -> [[Throat Center|Throat]],
  [[4/1]] -> [[Profile 4/1|4/1]], [[Type]] -> [[Energy Types|Type]], the four
  Quarter of X links and The Four Quarters -> [[Quarters|...]], all
  Juxtaposition / Left Angle / Right Angle variants -> [[Angles Overview|...]],
  Abstract and Logic Circuit -> Collective Circuit, Knowing Circuit ->
  Individual Circuit, Integration Channels -> Integration Circuit,
  BodyGraph -> Nine Centers. [[Rave New Year]] in gate-41 had no article and
  was dropped from the Related row.
- FACTUAL CORRECTION: four Cross of Planning articles (right-angle 1, 3, 4 and
  left-angle 2) called gates 9 and 16 "the Channel 9/16 of Identification".
  No such channel exists (9 pairs with 52, 16 with 48). In this cross 9 and 16
  are the Sun/Earth opposition pair. Reworded to "the 9/16 Sun/Earth axis" and
  the dead link was removed from 12 Related rows.

Still true after the pass, and fine:
- 106 frontmatter titles still contain em dashes (e.g. "Gate 21 — Biting
  Through / ..."). verify only checks the body, and those titles are wikilink
  targets, so they were left alone on purpose. Renaming them is a separate
  decision that would touch aliases and every inbound link.
- build.js still reports 194 articles reachable but not in the sidebar. That
  is the curated state, not a regression.

Variables section rebuilt (first session, 09.12.26). It went from 3 articles / 1,507 words to 40 articles /
63,033 words in one pass, all mined live from the Human Design Brain library.
Commit eb1713e, pushed, confirmed live.

What landed:
- variables/four-arrows (mechanics) and variables/four-transformations (process)
- 5 category pages: determination, environment, perspective, motivation, cognition
- 30 value pages, slugs variables/<category>-<value>
- variables-overview rewritten as the section front door
- content/variables.md rewritten as the section index

Corrections made to existing articles, worth knowing about:
- variables-overview had the arrow map wrong. Top left is Determination (not
  Motivation), bottom right is Perspective (not PHS), and Cognition is read from
  TONE and is not a fifth arrow at all. Also dropped an unsourced claim that Ra
  taught Variables as the "fourth line" of deconditioning.
- phs-diet carried a fabricated Ra Uru Hu quote labelled "(paraphrased)" that
  appears nowhere in the library. Removed.

NAMING SCHEME, decided 09.12.26, do not re-open without reason:
Every value page is titled "<Category>: <Value>", for example "Determination:
Appetite", "Cognition: Taste", "Perspective: Power". Slugs match. This was chosen
because three names could not resolve alone: "Power" was already aliased to
channels/34-57, and "Taste" and "Touch" each appear under two categories.
Qualified titles mean nothing is shadowed and nothing was renamed.
aliases.json also gained 19 bare-name aliases for the unambiguous values
(appetite, thirst, caves, kitchens, markets, mountains, shores, valleys,
survival, possibility, probability, wanting, personal, desire, guilt, innocence,
smell, inner vision, outer vision) plus view, digestion, dietary regimen,
strategic cognition, phs diet, primary health system, and the two structure
pages. The ambiguous names (light, sound, taste, touch, fear, hope, need,
feeling, power) were deliberately LEFT UNALIASED so they do not hijack ordinary
prose links elsewhere in the wiki.

STILL OPEN

1. SIDEBAR NAV is DONE. Approved in chat and applied 09.12.26 (commit 906e221).
   The Variables section now has 47 entries: seven dividers (Start Here, the five
   categories, Also Here) and 40 articles, with values numbered 1 to 6. No other
   nav section was touched. 194 articles elsewhere in the wiki are still
   reachable but not in the sidebar; that is the long-standing curated state, not
   a regression from this work.

2. BINDER SIDE, for a future "Both" session, never in a Wiki-only session.
   The binder's Who Has What page resolves a Variable value by looking up the
   lowercase value name in the wiki link map and accepting it only if the result
   starts with variables/. With the 19 bare aliases, 19 of the 30 values now
   resolve. Eleven stay dark: Determination Light / Sound / Taste / Touch,
   Perspective Power, Motivation Fear / Hope / Need, Cognition Taste / Touch /
   Feeling. The fix is one change on the binder side: look up
   "<category>: <value>" first and fall back to the bare name. That lights all
   30 permanently and is future-proof. Do not change the binder from a Wiki-only
   session.

3. CLEANUP PASS is DONE (commit b27df21, second session 09.12.26). verify
   content is 0 of 428 with problems. Keep it that way: run verify before every
   commit.

4. definition-types.md sits in variables/ but Definition is not a Variable; it
   belongs with Circuits. It also carries population percentages (41/46/11/1)
   that were not re-checked this session. Left where it is, flagged.

5. THIN SPOTS in the library, reported honestly in the articles rather than
   padded: Environment overall (Ra's "Orientation" lecture is essentially the
   only primary source), plus Perspective Wanting, Perspective Probability,
   Motivation Guilt, Motivation Innocence, Environment Kitchens, Environment
   Mountains, Determination Appetite, Determination Thirst, Cognition Inner
   Vision and Cognition Outer Vision. Several Ra books (Post Graduate Rave
   Psychology, Holistic Analysis 2) exist in the library as tables of contents
   only, with chapter titles like "The 2nd Color: Possibility" and "Perspective
   is a Prana" but no body text. Getting those bodies into the library would be
   the single biggest upgrade available to this section.

TOOLING NOTES, worth knowing
Pushing from a Cowork session: connecting ~/Developer/human-design-wiki as a
folder gives a fast Linux workspace for editing, verify and build.js, but that
workspace has no git identity and no GitHub credentials, and it cannot delete
files (a stale .git/index.lock needs delete permission or Desktop Commander).
Commit there with explicit -c user.name/user.email matching prior commits
(theshelbyinbox), then push and run gh from Desktop Commander, which runs on the
Mac proper. Also: `git stash` from the workspace can leave a stale index.lock.

tools/hdwiki.py mine splits source files on blank lines and drops any paragraph
over a size limit. Ra's mp3 transcripts are single 40KB paragraphs with no blank
lines, so mine silently returned almost nothing for them and still reported
success. Its --cap is a BYTE cap, not a passage count. Reading the whole library
from the sandbox VM also fails on many Google Drive files with EDEADLK, and the
script's try/except skipped them without saying so. Mine from the Mac, chunk long
paragraphs with a sliding window, and always check the read-failure count.
A working miner from the 09.12.26 session is kept in .corpus-variables/ (gitignored).
```
