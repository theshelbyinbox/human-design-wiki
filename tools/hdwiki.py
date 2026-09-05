#!/usr/bin/env python3
"""
hdwiki.py -- tooling for the Human Design Wiki.

The Human Design source library in Google Drive is a LIVING collection that
Shelby adds to continuously. Nothing in this file caches what that library
says. Every subcommand rescans it at run time, so the tooling stays correct
as the library grows.

Subcommands
-----------
  library   Report what the source library currently holds.
  gaps      What is in the library that the wiki may not cover yet.
  mine      Build a per-topic research corpus from the library.
  links     Emit the list of valid [[wikilink]] targets.
  verify    Check articles for frontmatter, links, em dashes, tables.

Run `python3 tools/hdwiki.py <cmd> --help` for options.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

# --- Defaults -------------------------------------------------------------
# The repo lives on local disk. The library lives in Google Drive and is
# read-only as far as this tooling is concerned.

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Escaped rather than literal: these path segments carry dingbats and emoji
# (U+278C, U+2605, U+1F9EC, U+1F9E0) that are easy to corrupt when copied.
_LIB_TAIL = ("➌ Resources/★ Wikipedia/"
             "02 Human Design \U0001f9ec/\U0001f9e0 Human Design Brain")

_LIB_CANDIDATES = [
    os.environ.get("HD_LIBRARY", ""),
    os.path.expanduser(
        "~/Library/CloudStorage/GoogleDrive-theshelby.inbox@gmail.com/"
        "My Drive/" + _LIB_TAIL),
    # When this repo is reached through a sandbox mount, the library is
    # usually mounted as a sibling by its leaf folder name.
    os.path.join(os.path.dirname(REPO), "02 Human Design \U0001f9ec",
                 "\U0001f9e0 Human Design Brain"),
    os.path.join(os.path.dirname(REPO), "\U0001f9e0 Human Design Brain"),
]


def _default_library():
    for c in _LIB_CANDIDATES:
        if c and os.path.isdir(c):
            return c
    return _LIB_CANDIDATES[1]


LIBRARY = _default_library()

TEXT_EXT = (".md", ".txt")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".obsidian"}


def _walk_library(library):
    """Every readable text file in the library, right now."""
    out = []
    for root, dirs, files in os.walk(library):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            if fn.lower().endswith(TEXT_EXT) and not fn.startswith("."):
                out.append(os.path.join(root, fn))
    return sorted(out)


def _read(path, limit=None):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(limit) if limit else f.read()
    except OSError:
        return ""


def _require_library(library):
    if not os.path.isdir(library):
        sys.exit(
            "Source library not found:\n  %s\n\n"
            "If the path changed, pass --library. Note that Google Drive files\n"
            "may be cloud-only until opened; if reads come back empty, open the\n"
            "folder in Finder once to materialise it." % library
        )


# --- library --------------------------------------------------------------

def cmd_library(a):
    _require_library(a.library)
    files = _walk_library(a.library)
    by_top, total_bytes, newest = {}, 0, []
    for p in files:
        rel = os.path.relpath(p, a.library)
        top = rel.split(os.sep)[0]
        try:
            st = os.stat(p)
        except OSError:
            continue
        by_top.setdefault(top, [0, 0])
        by_top[top][0] += 1
        by_top[top][1] += st.st_size
        total_bytes += st.st_size
        newest.append((st.st_mtime, rel))

    print("SOURCE LIBRARY: %s" % a.library)
    print("scanned %s: %d text files, %.1f MB\n"
          % (datetime.now().strftime("%Y-%m-%d %H:%M"), len(files), total_bytes / 1e6))
    print("By top-level folder:")
    for top in sorted(by_top, key=lambda k: -by_top[k][0]):
        n, b = by_top[top]
        print("  %-42s %5d files  %7.1f MB" % (top[:42], n, b / 1e6))

    newest.sort(reverse=True)
    print("\n%d most recently modified:" % min(a.recent, len(newest)))
    for mt, rel in newest[: a.recent]:
        print("  %s  %s" % (datetime.fromtimestamp(mt).strftime("%Y-%m-%d"), rel))


# --- gaps -----------------------------------------------------------------

def _wiki_articles():
    """Slug -> title for every article the site actually serves."""
    out = {}
    content = os.path.join(REPO, "content")
    for root, dirs, files in os.walk(content):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            m = re.search(r'^title:\s*"?([^"\n]+)"?', _read(p, 800), re.M)
            rel = os.path.relpath(p, content)
            out[rel[:-3]] = (m.group(1).strip() if m else fn[:-3])
    return out


def _last_content_change():
    try:
        ts = subprocess.run(
            ["git", "-C", REPO, "log", "-1", "--format=%ct", "--", "content"],
            capture_output=True, text=True, timeout=30).stdout.strip()
        return float(ts) if ts else None
    except Exception:
        return None


def cmd_gaps(a):
    _require_library(a.library)
    files = _walk_library(a.library)
    arts = _wiki_articles()
    titles = {t.lower() for t in arts.values()}
    slugs = {s.split("/")[-1].lower() for s in arts}

    since = a.since_ts if a.since_ts else _last_content_change()
    label = ("since the last content commit (%s)"
             % datetime.fromtimestamp(since).strftime("%Y-%m-%d")) if since else "(no baseline)"

    print("GAP CHECK")
    print("library : %s" % a.library)
    print("wiki    : %d articles in content/\n" % len(arts))

    # 1. Source files newer than the wiki's last content change.
    if since:
        fresh = []
        for p in files:
            try:
                st = os.stat(p)
            except OSError:
                continue
            if st.st_mtime > since:
                fresh.append((st.st_mtime, os.path.relpath(p, a.library)))
        fresh.sort(reverse=True)
        print("--- Source files added or changed %s: %d ---" % (label, len(fresh)))
        for mt, rel in fresh[: a.limit]:
            print("  %s  %s" % (datetime.fromtimestamp(mt).strftime("%Y-%m-%d"), rel))
        if len(fresh) > a.limit:
            print("  ... and %d more (raise --limit)" % (len(fresh) - a.limit))
        print("  NOTE: Drive can rewrite mtimes on sync, so treat this as a lead,")
        print("        not proof. Confirm by reading the files.")
    else:
        print("--- No git baseline found; skipping the recency check ---")

    # 2. Library subfolders whose subject has no obvious article.
    print("\n--- Library folders with no obviously matching article ---")
    seen = set()
    for p in files:
        rel = os.path.relpath(p, a.library)
        parts = rel.split(os.sep)
        if len(parts) < 2:
            continue
        # Everything under Source Material is provenance (book, course and
        # teacher names), never a wiki subject. Skip it or the list is noise.
        if parts[0].lower().startswith("source material") and not a.all_folders:
            continue
        folder = parts[-2]
        if folder in seen:
            continue
        seen.add(folder)
        probe = re.sub(r"^\d+[\.\s-]*", "", folder).strip().lower()
        if not probe or len(probe) < 4:
            continue
        if probe in titles or probe.replace(" ", "-") in slugs:
            continue
        if any(probe in t or t in probe for t in titles):
            continue
        print("  %s" % rel[: rel.rfind(os.sep)])
    print("\nThis is a prompt for judgement, not a to-do list. Many library")
    print("folders are teacher or course names, not wiki subjects.")


# --- mine -----------------------------------------------------------------

def _paragraphs(text, hard=3500, chunk=2800):
    out = []
    for p in re.split(r"\n\s*\n", text):
        p = p.strip()
        if not p:
            continue
        if len(p) > hard:
            out.extend(p[i:i + chunk] for i in range(0, len(p), chunk))
        else:
            out.append(p)
    return out


def cmd_mine(a):
    _require_library(a.library)
    core = [re.compile(t.strip(), re.I) for t in a.terms.split(",") if t.strip()]
    supp = [re.compile(t.strip(), re.I) for t in (a.also or "").split(",") if t.strip()]
    if not core:
        sys.exit("--terms is required, e.g. --terms 'gate 41,the root'")

    files = _walk_library(a.library)
    os.makedirs(a.out, exist_ok=True)

    # Whole documents whose FILENAME matches -- contiguous teaching beats fragments.
    prim = []
    if a.primary:
        keys = [k.strip().lower() for k in a.primary.split(",") if k.strip()]
        stems = set()
        for p in files:
            base = os.path.basename(p).lower()
            if any(k in base for k in keys):
                stem = os.path.splitext(p)[0]
                if stem not in stems:
                    stems.add(stem)
                    prim.append(p)
        prim.sort()
        total = 0
        pf = os.path.join(a.out, "%s__primary.txt" % a.name)
        with open(pf, "w", encoding="utf-8") as o:
            o.write("# PRIMARY SOURCES for '%s'\n# scanned %s from %s\n"
                    % (a.name, datetime.now().strftime("%Y-%m-%d"), a.library))
            for p in prim:
                if total > a.primary_cap:
                    break
                t = _read(p)[: a.per_file]
                o.write("\n\n========== FILE: %s ==========\n\n%s\n"
                        % (os.path.relpath(p, a.library), t))
                total += len(t)
        print("primary   : %d files, %d bytes -> %s" % (len(prim), total, os.path.basename(pf)))

    # Scored fragments from everything else.
    prim_set = set(prim)
    hits, seen = [], set()
    for p in files:
        if p in prim_set:
            continue
        rel = os.path.relpath(p, a.library)
        for para in _paragraphs(_read(p)):
            if len(para) < a.min_len:
                continue
            low = para.lower()
            nc = sum(1 for r in core if r.search(low))
            if not nc:
                continue
            ns = sum(1 for r in supp if r.search(low))
            h = hashlib.md5(re.sub(r"\s+", " ", low).encode()).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            hits.append((nc * 3 + ns, rel, para))

    hits.sort(key=lambda x: -x[0])
    kept, total, perfile = [], 0, {}
    for sc, rel, para in hits:
        if perfile.get(rel, 0) >= a.per_source:
            continue
        if total + len(para) > a.cap:
            continue
        kept.append((sc, rel, para))
        total += len(para) + 90
        perfile[rel] = perfile.get(rel, 0) + 1

    ff = os.path.join(a.out, "%s__fragments.txt" % a.name)
    with open(ff, "w", encoding="utf-8") as f:
        f.write("# FRAGMENTS for '%s': %d passages from %d files\n"
                "# scanned %s across %d library files\n"
                % (a.name, len(kept), len(perfile),
                   datetime.now().strftime("%Y-%m-%d"), len(files)))
        for sc, rel, para in kept:
            f.write("\n[SOURCE: %s]\n%s\n" % (rel, para))
    print("fragments : %d of %d candidates, %d files, %d bytes -> %s"
          % (len(kept), len(hits), len(perfile), total, os.path.basename(ff)))
    if len(hits) > len(kept):
        print("            %d candidates dropped by --cap; raise it to widen."
              % (len(hits) - len(kept)))


# --- links ----------------------------------------------------------------

def _valid_targets():
    titles = set()
    mf = os.path.join(REPO, "manifest.json")
    if os.path.exists(mf):
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ("label", "title") and isinstance(v, str):
                        titles.add(v)
                    walk(v)
            elif isinstance(o, list):
                for i in o:
                    walk(i)
        try:
            walk(json.load(open(mf)))
        except Exception:
            pass
    titles.update(_wiki_articles().values())
    af = os.path.join(REPO, "aliases.json")
    if os.path.exists(af):
        try:
            titles.update(json.load(open(af)).keys())
        except Exception:
            pass
    return titles


def cmd_links(a):
    t = sorted(_valid_targets())
    text = ("# Valid [[wikilink]] targets. Use ONLY these.\n"
            "# generated %s -- %d targets\n\n%s\n"
            % (datetime.now().strftime("%Y-%m-%d"), len(t), "\n".join(t)))
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
        print("wrote %d targets -> %s" % (len(t), a.out))
    else:
        sys.stdout.write(text)


# --- verify ---------------------------------------------------------------

def cmd_verify(a):
    try:
        import yaml
    except ImportError:
        yaml = None
    valid = {t.lower() for t in _valid_targets()}
    paths = []
    for target in a.paths:
        if os.path.isdir(target):
            for root, dirs, files in os.walk(target):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                paths += [os.path.join(root, f) for f in files if f.endswith(".md")]
        elif target.endswith(".md"):
            paths.append(target)
    paths.sort()
    if not paths:
        sys.exit("No .md files found in: %s" % ", ".join(a.paths))

    print("%-34s %6s %5s %3s %3s  %s"
          % ("FILE", "WORDS", "LINKS", "EM", "TBL", "PROBLEMS"))
    fails = 0
    for p in paths:
        t = _read(p)
        m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
        body = t[m.end():] if m else t
        problems = []
        if not m:
            problems.append("no frontmatter")
        elif yaml:
            try:
                fm = yaml.safe_load(m.group(1))
                if not isinstance(fm, dict) or "title" not in fm:
                    problems.append("frontmatter missing title")
            except Exception as e:
                problems.append("invalid YAML (%s)" % type(e).__name__)

        links = re.findall(r"\[\[([^\]]+)\]\]", body)
        bad = sorted({l.split("|")[0].strip() for l in links
                      if l.split("|")[0].strip().lower() not in valid})
        if bad:
            problems.append("bad links: " + ", ".join(bad[:4]))

        # Em dashes are allowed inside wikilinks, since some article titles use them.
        prose = re.sub(r"\[\[[^\]]+\]\]", "", body)
        em = prose.count("—") + prose.count("–")
        if em:
            problems.append("%d em dash(es) in prose" % em)

        tbl = len(re.findall(r"^\s*\|.*\|\s*$", body, re.M))
        if tbl:
            problems.append("%d table row(s)" % tbl)

        dupes = [h for h in set(re.findall(r"^#{2,3} .+$", body, re.M))
                 if body.count(h + "\n") > 1]
        if dupes:
            problems.append("duplicate heading: %s" % dupes[0].strip())

        words = len(re.sub(r"[#*\[\]|]", " ", body).split())
        if problems:
            fails += 1
        print("%-34s %6d %5d %3d %3d  %s"
              % (os.path.basename(p)[:34], words, len(links), em, tbl,
                 "; ".join(problems) if problems else "ok"))

    print("\n%d file(s) checked, %d with problems." % (len(paths), fails))
    if yaml is None:
        print("NOTE: PyYAML not installed, so YAML validity was not checked.")
    return 1 if fails else 0


# --- main -----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_lib(p):
        p.add_argument("--library", default=LIBRARY, help="Source library root.")

    p = sub.add_parser("library", help="Report what the source library holds.")
    add_lib(p)
    p.add_argument("--recent", type=int, default=15)
    p.set_defaults(fn=cmd_library)

    p = sub.add_parser("gaps", help="What the library has that the wiki may not.")
    add_lib(p)
    p.add_argument("--limit", type=int, default=40)
    p.add_argument("--since-ts", type=float, default=None,
                   help="Unix timestamp baseline; defaults to last content commit.")
    p.add_argument("--all-folders", action="store_true",
                   help="Include Source Material folders, normally skipped as provenance.")
    p.set_defaults(fn=cmd_gaps)

    p = sub.add_parser("mine", help="Build a research corpus for one topic.")
    add_lib(p)
    p.add_argument("--name", required=True, help="Slug for the output files.")
    p.add_argument("--terms", required=True,
                   help="Comma-separated regexes. A paragraph must match one.")
    p.add_argument("--also", default="",
                   help="Comma-separated regexes that raise a passage's rank.")
    p.add_argument("--primary", default="",
                   help="Comma-separated FILENAME substrings to include whole.")
    p.add_argument("--out", required=True, help="Output directory.")
    p.add_argument("--cap", type=int, default=190000)
    p.add_argument("--primary-cap", type=int, default=230000)
    p.add_argument("--per-file", type=int, default=60000)
    p.add_argument("--per-source", type=int, default=25)
    p.add_argument("--min-len", type=int, default=150)
    p.set_defaults(fn=cmd_mine)

    p = sub.add_parser("links", help="Emit valid wikilink targets.")
    p.add_argument("--out", default=None)
    p.set_defaults(fn=cmd_links)

    p = sub.add_parser("verify", help="Check articles before committing.")
    p.add_argument("paths", nargs="+")
    p.set_defaults(fn=cmd_verify)

    a = ap.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
