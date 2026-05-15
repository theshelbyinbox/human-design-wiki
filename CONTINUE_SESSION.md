# Continuation Prompt — Human Design Wiki

Paste the prompt below into a new Claude session to pick up where this conversation left off. It tells Claude where the project lives, what's been built, and how the system is structured.

---

## Prompt to paste:

```
I'm continuing work on my Human Design Wiki. Here's everything you need to get up to speed.

PROJECT LOCATION
- Local working folder: /Users/shelbymanzano/Documents/The Journey/*Human Design Brain/wiki
  (note: the parent folder name starts with a literal asterisk — always quote the path)
- Source material folders (HD content I draw from): /Users/shelbymanzano/Documents/The Journey/*Human Design Brain/01. Core Concepts through 10. Variables PHS & Advanced
- GitHub repo: https://github.com/theshelbyinbox/human-design-wiki
- Live site: https://theshelbyinbox.github.io/human-design-wiki/
- GitHub auth: gh CLI is already logged in as theshelbyinbox with repo scope
- Repo-local git email: 222821948+theshelbyinbox@users.noreply.github.com (already set — don't change)

ARCHITECTURE
The wiki is a single-file SPA. index.html contains everything: HTML shell, CSS,
all article content, and the routing JS. There are three coupled data structures
inside index.html that must stay in sync when adding/renaming/removing pages:

1. const articles = { } — keyed by path string (e.g., "strategy/respond" or just
   "strategy" for section pages). Each article has: title, section, related,
   content (markdown in a JS template literal — NO backticks allowed in content).
2. const navSections = [ ] — manually ordered sidebar; each section has key, label,
   and an articles array of {key, label}.
3. const wikilinkMap = { } — lowercase title → path; resolves [[X]] references.
   Has fallback partial-match logic in resolveWikilink().

WHEN ADDING PAGES: update all three. When renaming a path: update key in articles,
key in navSections, value in wikilinkMap. JS object literal duplicate keys silently
let the last one win — watch for accidental duplicates.

NO BACKTICKS rule: article.content is a JS template literal delimited by backticks.
Any backtick inside content breaks the JS. When drawing from sources, strip them.

CURRENT STATE (as of 2026-05-15)
- 71 articles, 10 sections.
- Sections (in sidebar order): Core Concepts (5), Strategy (7), Inner Authority (12),
  Energy Types (5), Centers (10), Profiles & Lines (14), Gates (2), Channels (1),
  Incarnation Cross (2), Variables & PHS (3).
- Each section has a CLICKABLE LANDING PAGE at a single-segment URL:
  #/concepts, #/strategy, #/inner-authority, #/types, #/centers, #/profiles,
  #/gates, #/channels, #/incarnation-crosses, #/variables.
- Section landing pages are keyed by just the section key (no slash). Source
  markdown for each lives at {section}/section.md.
- Sidebar pattern: split header — clickable <a class="sidebar-section-title">
  navigates to section page; separate <button class="chevron-btn"> toggles
  collapse. Don't combine them.
- Breadcrumb: section pages show "Home › Section". Sub-pages show
  "Home › Section › Article" with the middle Section as a clickable link.
- In-page Contents (TOC) uses onclick="scrollToSection('slug')" NOT href="#slug"
  because the SPA hash-router treats #anchor as a malformed route. H2/H3 renderer
  adds id="slug" to headings.
- The home page has a "View All Sections" grid with 10 cards linking to each
  section landing page. Cards use onclick navigation (not nested anchors) and
  the title is a clickable <a> overlapping the same target.

WIKILINK SEMANTICS
- [[Strategy]] and [[Inner Authority]] route to their SECTION PAGES (broader concept).
- [[Strategy Overview]] and [[Inner Authority Overview]] route to the specific content overview articles.
- All bare section names also resolve: [[Centers]], [[Energy Types]], [[Gates]],
  [[Channels]], [[Profiles & Lines]], [[Incarnation Cross]], [[Variables & PHS]],
  [[Core Concepts]].
- Only known unresolved wikilink in the wiki: [[BodyGraph]] (renders as plain text,
  no page exists — conceptual term).

RECENT MAJOR CHANGES (most recent first)
- Added View All Sections grid on home page (cards link to section landing pages).
- Created 10 section landing pages with brief intro + sub-page list + related sections.
- Fixed Profile X-Y wikilink resolution (added 24 aliases for both dash and slash formats).
- Scrubbed orphan wikilinks ([[Ra Uru Hu]], [[Jovian Archive]], [[Transits]]) after
  removing Teachers and Applications sections — prose got brackets stripped, pipe-list
  entries got removed entirely.
- Removed Teachers and Applications sections entirely (Shelby's call).
- Removed duplicate chip-style "Related Articles" box at bottom of every page
  (each article already has a pipe-separated Related Articles section in its content).
- Fixed in-page Contents links navigating to "Not Found" (switched from href=#slug
  to onclick=scrollToSection).
- Promoted Strategy and Inner Authority from inside Core Concepts to their own
  top-level sections; merged Authorities section under Inner Authority.
- Initial repo creation, pushed to GitHub Pages, fixed GH007 email privacy block
  via noreply email.

PERSISTENT MEMORY FILES IN CLAUDE
These memory files capture the design decisions for future sessions:
- ~/.claude/projects/-Users-shelbymanzano/memory/project_hd_wiki_live.md
  (current state, SPA architecture, section landing pattern, breadcrumb logic,
  wikilink semantics)
- ~/.claude/projects/-Users-shelbymanzano/memory/reference_github_pages_first_push.md
  (GitHub Pages deploy recipe + GH007 fix)
- ~/.claude/projects/-Users-shelbymanzano/memory/reference_preview_smooth_scroll.md
  (Claude Code preview env doesn't honor behavior:'smooth' — use legacy fallback)

WORKFLOW
When making changes:
1. Edit index.html and/or markdown source files.
2. Validate JS syntax: extract the script block and run `node -c`.
3. Verify in the preview (preview_start with name "hd-wiki" — already in
   /Users/shelbymanzano/Documents/.claude/launch.json).
4. Commit with descriptive message + push to main.
5. GitHub Pages auto-rebuilds in ~40s.

OPEN POSSIBILITIES (things we discussed but haven't built)
- Alias [[BodyGraph]] to centers/nine-centers to close the last unresolved wikilink.
- Add more sub-pages and content to Variables & PHS section (Shelby plans to expand
  this later).

CONTEXT ABOUT ME
- I'm Shelby (theshelbyinbox on GitHub).
- I'm a non-linear worker — bursts then rest. Don't give time-based schedules.
- End every response with a directional question/invitation ("Want to tackle X?"),
  not a statement.
- Use headings, bullet points, tables. No walls of text. No emojis.

Please orient yourself by reading the memory files above, then ask me what
I want to work on next.
```

---

## How to use this prompt

1. Open a new Claude Code session (or any Claude session with access to your files and GitHub).
2. Paste the entire fenced prompt above.
3. Claude will read the memory files and orient itself, then ask what's next.
