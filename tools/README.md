# tools/

Helpers for writing wiki articles out of the Human Design source library.

## The one principle

The source library in Google Drive is a **living collection** that grows
continuously. Nothing here caches what it says. Every command rescans the
library at run time, so the tooling stays correct as new transcripts, books
and course material arrive.

Never copy Human Design facts into a script, a skill, or a note and treat
them as current. Read the library.

## Where things are

- **Repo (this folder's parent):** `~/Developer/human-design-wiki`
  Local disk. Never a synced folder. See the warning in the root README.
- **Source library:** Google Drive, `➌ Resources/★ Wikipedia/02 Human Design 🧬/🧠 Human Design Brain/`
  Read from it. Never write to it, and never put a git repo inside it.
- Override the library path with `--library` or the `HD_LIBRARY` env var.

## Commands

    python3 tools/hdwiki.py library
Report what the library currently holds: file counts by folder, total size,
and the most recently modified files. Run this first in any session, since
it shows what changed since last time.

    python3 tools/hdwiki.py gaps
Two questions at once. What source files changed since the wiki's last
content commit, and which library subjects have no obviously matching
article. Folders under `Source Material` are skipped as provenance rather
than subjects; add `--all-folders` to include them. Output is a prompt for
judgement, not a to-do list.

    python3 tools/hdwiki.py mine --name <slug> --terms <regexes> --out <dir>
Build a research corpus for one topic. Produces two files:

- `<slug>__primary.txt` — whole documents whose *filename* matched
  `--primary`. Contiguous teaching, which reads far better than fragments.
- `<slug>__fragments.txt` — the highest-scoring passages from everything
  else, deduplicated, capped per source file so one book cannot dominate.

A paragraph must match at least one `--terms` regex to be considered.
`--also` regexes do not admit a passage; they raise its rank. Raise `--cap`
if the run reports many dropped candidates and the topic deserves more.

    python3 tools/hdwiki.py links --out valid-links.txt
Emit every valid `[[wikilink]]` target, from `manifest.json`, article
frontmatter, and `aliases.json`. Give this to anyone writing articles so
they cannot invent link targets.

    python3 tools/hdwiki.py verify content/<section>
Check articles before committing: frontmatter present and valid YAML, no
unknown wikilinks, no em dashes in prose, no markdown tables, no duplicate
headings. Exits non-zero if anything fails. Em dashes *inside* wikilinks are
allowed, because some article titles legitimately contain them.

## Conventions the verifier enforces

- Frontmatter on every article. In `content/`: `title`, `section`, `related`.
- No em dashes in prose. The wiki's dash is ` -- `.
- No markdown tables anywhere. Use headings and bullets.
- Wikilinks only to targets that actually exist.

## Requirements

Python 3 and PyYAML (`python3 -m pip install --user PyYAML`). Without
PyYAML the verifier still runs but skips YAML validity checking and says so.
