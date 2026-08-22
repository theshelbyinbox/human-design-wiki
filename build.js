#!/usr/bin/env node
// ============================================================
// WIKI BUILD SCRIPT — regenerates manifest.json + search-index.json
// from the content/ markdown tree. Run after adding/editing articles:
//   node build.js
// Nav order: existing manifest.json order is preserved (curated). New
// articles are reported but NOT auto-added to the sidebar; pass --add-nav
// to append them, or edit manifest.json navSections by hand.
// Wikilinks: lowercase titles are auto-mapped; extra aliases live in
// aliases.json (edit by hand to add nicknames like "gate 1").
// ============================================================
const fs = require('fs'), path = require('path');

function walk(d) {
  return fs.readdirSync(d, { withFileTypes: true }).flatMap(e =>
    e.isDirectory() ? walk(path.join(d, e.name)) :
    e.name.endsWith('.md') ? [path.join(d, e.name)] : []);
}
function parseFrontmatter(raw) {
  if (!raw.startsWith('---')) return { meta: {}, content: raw };
  const end = raw.indexOf('\n---', 3);
  if (end < 0) return { meta: {}, content: raw };
  const meta = {};
  for (const line of raw.slice(3, end).split('\n')) {
    const m = line.match(/^(\w[\w-]*):\s*(.*)$/);
    if (!m) continue;
    let v = m[2].trim();
    try { v = JSON.parse(v); } catch (e) {}
    meta[m[1]] = v;
  }
  return { meta, content: raw.slice(end + 4).replace(/^\n+/, '') };
}

const old = fs.existsSync('manifest.json') ? JSON.parse(fs.readFileSync('manifest.json', 'utf8')) : {};
const aliases = fs.existsSync('aliases.json') ? JSON.parse(fs.readFileSync('aliases.json', 'utf8')) : {};

const articles = {};
for (const p of walk('content')) {
  const key = p.replace(/^content\//, '').replace(/\.md$/, '');
  const { meta, content } = parseFrontmatter(fs.readFileSync(p, 'utf8'));
  articles[key] = {
    title: meta.title || key.split('/').pop(),
    section: meta.section || key.split('/')[0],
    content
  };
}

// nav: preserve old order, append new keys, drop deleted
const navSections = (old.navSections || []).map(s => ({
  ...s,
  articles: s.articles.filter(a => a.divider || articles[a.key])
}));
const known = new Set(navSections.flatMap(s => s.articles.map(a => a.key).filter(Boolean)));
navSections.forEach(s => { if (articles[s.key]) known.add(s.key); });
const unlisted = [];
for (const key of Object.keys(articles).sort()) {
  if (known.has(key)) continue;
  const sectionKey = key.includes('/') ? key.split('/')[0] : key;
  if (key === sectionKey) continue; // section landing pages live in nav headers
  if (process.argv.includes('--add-nav')) {
    let sec = navSections.find(s => s.key === sectionKey);
    if (!sec) { sec = { key: sectionKey, label: sectionKey, articles: [] }; navSections.push(sec); }
    sec.articles.push({ key, label: articles[key].title });
    console.log('nav: appended', key);
  } else {
    unlisted.push(key);
  }
}
if (unlisted.length) console.log('note:', unlisted.length, 'articles are reachable by link/search but not in the sidebar (curated nav). Use --add-nav to append them, or edit manifest.json by hand.');

// wikilinks: auto titles + manual aliases (aliases win only if target exists)
const wikilinkMap = {};
for (const [key, a] of Object.entries(articles)) wikilinkMap[a.title.toLowerCase()] = key;
for (const [k, v] of Object.entries(aliases)) if (articles[v]) wikilinkMap[k] = v;

const meta = {};
for (const [key, a] of Object.entries(articles)) meta[key] = { title: a.title, section: a.section };

const manifest = {
  generated: new Date().toISOString().slice(0, 10),
  wiki: old.wiki || { name: 'Wiki', tagline: '' },
  navSections, articles: meta, wikilinkMap
};
fs.writeFileSync('manifest.json', JSON.stringify(manifest, null, 1));

const idx = {};
for (const [key, a] of Object.entries(articles)) {
  idx[key] = { t: a.title, s: a.section, x: a.content.replace(/[#*`|\[\]]/g, ' ').replace(/\s+/g, ' ').trim() };
}
fs.writeFileSync('search-index.json', JSON.stringify(idx));

console.log('built:', Object.keys(articles).length, 'articles,', navSections.length, 'sections,', Object.keys(wikilinkMap).length, 'wikilinks');
