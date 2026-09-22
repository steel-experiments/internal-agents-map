#!/usr/bin/env node
// ABOUTME: Phase 3 of the SEO pulse: audits the head, structured data, and text of every published route.
// ABOUTME: It reports by route family, because one template defect appears on every page it generates.
// Usage: node .claude/skills/seo/scripts/tech-audit.mjs            # reads dist/, after "npm run build"
//        node .claude/skills/seo/scripts/tech-audit.mjs --live     # reads the production site
//        node .claude/skills/seo/scripts/tech-audit.mjs --family entry
// The checks here do not repeat scripts/check_site.py or scripts/check_delivery.py, which hold the
// structure, redirect, and header contract. This script holds the search-facing quality of the pages.
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { loadConfig, loadRoutes, familyOf, familyRules, monthStamp, writeSnapshot, latestSnapshot, pulsePath, log } from './_lib.mjs';

const config = loadConfig();
const month = monthStamp();
const rules = config.page_rules;
const live = process.argv.includes('--live');
const onlyFamily = process.argv.includes('--family') ? process.argv[process.argv.indexOf('--family') + 1] : null;
const distDir = pulsePath(config, 'dist_dir');

let routes = loadRoutes(config);
if (onlyFamily) routes = routes.filter((r) => familyOf(config, r.path) === onlyFamily);
if (!live && !existsSync(distDir)) {
  console.error(`${config.paths.dist_dir} is missing. Run "npm run build", or pass --live to read the production site.`);
  process.exit(1);
}

function pick(html, re) { const m = html.match(re); return m ? (m[1] ?? m[0]) : null; }
function decode(s) {
  return s ? s.replace(/&amp;/g, '&').replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#183;|&middot;/g, '·') : null;
}

/**
 * Count the words of the main element, not of the page.
 * The navigation, the search palette, and the footer are the same on every page, so
 * they would hide a page that holds almost no catalog text.
 */
function wordCount(html) {
  const main = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  const text = (main ? main[1] : html)
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<svg[\s\S]*?<\/svg>/gi, ' ')
    .replace(/<[^>]+>/g, ' ');
  return decode(text).split(/\s+/).filter(Boolean).length;
}

/** Collect the @type values of every node of every structured-data block. */
function jsonLdTypes(html) {
  const blocks = html.match(/<script[^>]*application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi) || [];
  const types = new Set();
  let broken = 0;
  for (const block of blocks) {
    const body = block.replace(/^[\s\S]*?>/, '').replace(/<\/script>$/i, '').replace(/\\u003c/g, '<');
    try {
      const data = JSON.parse(body);
      const nodes = Array.isArray(data['@graph']) ? data['@graph'] : [data];
      for (const node of nodes) if (node && node['@type']) types.add(String(node['@type']));
    } catch {
      broken += 1;
    }
  }
  return { types: [...types], blocks: blocks.length, broken };
}

async function readPage(route) {
  if (live) {
    const res = await fetch(config.origin + route.path, { redirect: 'follow', headers: { 'User-Agent': 'internal-agents-map seo audit' } });
    return { status: res.status, finalUrl: res.url, html: await res.text() };
  }
  const file = join(distDir, route.html.replace(/^\//, ''));
  if (!existsSync(file)) return { status: 404, html: '' };
  return { status: 200, html: readFileSync(file, 'utf8') };
}

async function auditRoute(route) {
  const out = { path: route.path, family: familyOf(config, route.path) };
  const family = familyRules(config, out.family);
  try {
    const page = await readPage(route);
    out.status = page.status;
    if (page.finalUrl && page.finalUrl !== config.origin + route.path) out.finalUrl = page.finalUrl;
    const html = page.html;
    out.title = decode(pick(html, /<title[^>]*>([^<]*)<\/title>/i));
    out.description = decode(pick(html, /<meta\s+name="description"\s+content="([^"]*)"/i));
    out.canonical = pick(html, /<link\s+rel="canonical"\s+href="([^"]*)"/i);
    out.robots = pick(html, /<meta\s+name="robots"\s+content="([^"]*)"/i);
    out.ogTitle = decode(pick(html, /<meta\s+property="og:title"\s+content="([^"]*)"/i));
    out.ogImage = pick(html, /<meta\s+property="og:image"\s+content="([^"]*)"/i);
    out.markdownAlternate = pick(html, /<link\s+rel="alternate"\s+type="text\/markdown"\s+href="([^"]*)"/i);
    out.h1 = (html.match(/<h1[\s>]/gi) || []).length;
    out.words = wordCount(html);
    const ld = jsonLdTypes(html);
    out.jsonld_types = ld.types;
    out.jsonld_blocks = ld.blocks;
    out.jsonld_broken = ld.broken;
  } catch (e) {
    out.fetchError = e.message;
  }

  const issues = [];
  const add = (sev, msg) => issues.push({ sev, msg });
  if (out.fetchError) add('critical', `the page could not be read: ${out.fetchError}`);
  if (out.status && out.status >= 400) add('critical', `HTTP ${out.status}`);
  if (out.finalUrl) add('high', `the canonical path redirects to ${out.finalUrl}`);
  if (!out.title) add('high', 'there is no title');
  else {
    if (out.title.length > rules.title_max) add('medium', `the title is ${out.title.length} characters, the limit is ${rules.title_max}`);
    if (rules.title_suffix && !out.title.endsWith(rules.title_suffix)) add('low', `the title does not end with "${rules.title_suffix}"`);
  }
  if (!out.description) add('high', 'there is no description');
  else {
    if (out.description.length < rules.description_min) add('medium', `the description is ${out.description.length} characters, the minimum is ${rules.description_min}`);
    if (out.description.length > rules.description_max) add('low', `the description is ${out.description.length} characters, the maximum is ${rules.description_max}`);
  }
  const expectedCanonical = config.origin + route.path;
  if (!out.canonical) add('high', 'there is no canonical link');
  else if (out.canonical !== expectedCanonical) add('high', `the canonical link is ${out.canonical}, the path is ${expectedCanonical}`);
  if (out.robots && /noindex/i.test(out.robots)) add('critical', `the page is noindex: ${out.robots}`);
  if (out.jsonld_broken) add('high', `${out.jsonld_broken} structured-data blocks do not parse`);
  if (out.jsonld_blocks === 0) add('high', 'there is no structured data');
  for (const type of family?.jsonld_types || []) {
    if (out.jsonld_types && !out.jsonld_types.includes(type)) add('medium', `the structured data has no ${type} node`);
  }
  if (out.h1 === 0) add('medium', 'there is no h1');
  else if (out.h1 > 1) add('low', `there are ${out.h1} h1 elements`);
  if (family?.min_words && out.words != null && out.words < family.min_words) {
    add('medium', `the page has ${out.words} words, the ${out.family} floor is ${family.min_words}`);
  }
  if (!out.markdownAlternate) add('low', 'there is no Markdown alternate link');
  if (rules.og_image_default && route.path !== '/') {
    if (!out.ogImage) add('medium', 'there is no og:image');
    else if (new URL(out.ogImage, config.origin).pathname === rules.og_image_default) add('medium', 'the page shares the default preview card');
  }
  out.issues = issues;
  return out;
}

const results = [];
for (const route of routes) {
  const r = await auditRoute(route);
  results.push(r);
  const worst = r.issues.find((i) => i.sev === 'critical') || r.issues.find((i) => i.sev === 'high');
  if (worst) log(`err ${r.path}: ${worst.msg}`);
}
log(`read ${results.length} routes from ${live ? config.origin : config.paths.dist_dir}`);

// --- defects that only appear across pages ---
function duplicates(field) {
  const groups = new Map();
  for (const r of results) {
    const value = r[field];
    if (!value) continue;
    if (!groups.has(value)) groups.set(value, []);
    groups.get(value).push(r.path);
  }
  return [...groups.entries()].filter(([, paths]) => paths.length > 1).map(([value, paths]) => ({ value, paths }));
}
const duplicateTitles = duplicates('title');
const duplicateDescriptions = duplicates('description');

// The sitemap must hold the same routes the build published: no more, no fewer.
let sitemap = null;
if (!live) {
  const sitemapPath = join(distDir, 'sitemap.xml');
  if (existsSync(sitemapPath)) {
    const listed = [...readFileSync(sitemapPath, 'utf8').matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(config.origin, ''));
    const published = new Set(loadRoutes(config).map((r) => r.path));
    sitemap = {
      missing: [...published].filter((p) => !listed.includes(p)),
      extra: listed.filter((p) => !published.has(p)),
    };
  }
}

// Only a complete run becomes the snapshot of the month: a run of one family would
// replace the baseline that the next month compares against.
const snapshot = { source: live ? 'live' : 'dist', pages: results, duplicateTitles, duplicateDescriptions, sitemap };
if (onlyFamily) log(`this run holds the ${onlyFamily} family only, so it does not write the snapshot of the month`);
else log(`wrote ${writeSnapshot(config, 'tech', month, snapshot)}`);

// --- the difference against the previous month ---
const prev = latestSnapshot(config, 'tech', month);
const changes = [];
if (prev?.data?.pages) {
  const prevMap = new Map(prev.data.pages.map((r) => [r.path, r]));
  const key = (i) => `${i.sev}:${i.msg}`;
  for (const r of results) {
    const p = prevMap.get(r.path);
    if (!p) { changes.push({ path: r.path, type: 'page added', family: r.family }); continue; }
    const now = new Set((r.issues || []).map(key));
    const was = new Set((p.issues || []).map(key));
    for (const i of now) if (!was.has(i)) changes.push({ path: r.path, type: 'new defect', detail: i });
    for (const i of was) if (!now.has(i)) changes.push({ path: r.path, type: 'defect resolved', detail: i });
    if (r.title !== p.title) changes.push({ path: r.path, type: 'title changed', detail: `${p.title} -> ${r.title}` });
  }
  if (!onlyFamily) {
    const paths = new Set(results.map((r) => r.path));
    for (const p of prev.data.pages) if (!paths.has(p.path)) changes.push({ path: p.path, type: 'page removed' });
  }
}

// --- the report on the terminal ---
const sev = (r, level) => r.issues.filter((i) => i.sev === level).length;
console.log(`\n# Technical audit, ${month} (${results.length} routes from ${live ? 'the live site' : config.paths.dist_dir}, previous: ${prev?.month || 'none'})`);
console.log('\nBy family:');
console.log('  family         pages  clean  critical  high  medium');
for (const family of [...config.route_families.map((f) => f.id), 'other']) {
  const group = results.filter((r) => r.family === family);
  if (!group.length) continue;
  const clean = group.filter((r) => !r.issues.some((i) => i.sev !== 'low')).length;
  const counts = ['critical', 'high', 'medium'].map((l) => group.reduce((s, r) => s + sev(r, l), 0));
  console.log(`  ${family.padEnd(14)} ${String(group.length).padStart(5)} ${String(clean).padStart(6)} ${String(counts[0]).padStart(9)} ${String(counts[1]).padStart(5)} ${String(counts[2]).padStart(7)}`);
}

// A defect that every page of a family carries is a template defect: report it once, not 56 times.
console.log('\nDefects:');
const byMessage = new Map();
for (const r of results) {
  for (const i of r.issues) {
    if (i.sev === 'low') continue;
    const k = `${r.family}|${i.sev}|${i.msg.replace(/\d+/g, 'N')}`;
    if (!byMessage.has(k)) byMessage.set(k, { family: r.family, sev: i.sev, msg: i.msg, paths: [] });
    byMessage.get(k).paths.push(r.path);
  }
}
const order = { critical: 0, high: 1, medium: 2 };
const grouped = [...byMessage.values()].sort((a, b) => order[a.sev] - order[b.sev] || b.paths.length - a.paths.length);
if (!grouped.length) console.log('  None above the low level.');
for (const g of grouped) {
  const total = results.filter((r) => r.family === g.family).length;
  const scope = g.paths.length === total ? `every ${g.family} page (${total})` : `${g.paths.length} of ${total} ${g.family} pages`;
  console.log(`  [${g.sev}] ${scope}: ${g.msg}`);
  if (g.paths.length < total) console.log(`      ${g.paths.slice(0, 5).join(', ')}${g.paths.length > 5 ? ` and ${g.paths.length - 5} more` : ''}`);
}

if (duplicateTitles.length || duplicateDescriptions.length) {
  console.log('\nRepeated head text (pages that compete with each other):');
  for (const d of duplicateTitles) console.log(`  title "${d.value}" on ${d.paths.length} pages: ${d.paths.slice(0, 4).join(', ')}`);
  for (const d of duplicateDescriptions) console.log(`  description on ${d.paths.length} pages: ${d.paths.slice(0, 4).join(', ')}`);
} else {
  console.log('\nNo title or description is repeated.');
}

if (sitemap) {
  if (sitemap.missing.length || sitemap.extra.length) {
    console.log('\nSitemap:');
    if (sitemap.missing.length) console.log(`  published but not listed: ${sitemap.missing.join(', ')}`);
    if (sitemap.extra.length) console.log(`  listed but not published: ${sitemap.extra.join(', ')}`);
  } else {
    console.log('\nThe sitemap holds every published route and nothing else.');
  }
}

const thin = results.filter((r) => r.words != null).sort((a, b) => a.words - b.words).slice(0, 8);
console.log('\nLeast text (candidates for more evidence, not for more words):');
for (const r of thin) console.log(`  ${String(r.words).padStart(5)} words  ${r.path}`);

if (changes.length) {
  console.log(`\nChanges against ${prev.month} (${prev.data.source}):`);
  for (const c of changes.slice(0, 40)) console.log(`  ${c.type}: ${c.path}${c.detail ? ` — ${c.detail}` : ''}`);
  if (changes.length > 40) console.log(`  and ${changes.length - 40} more, see the snapshot`);
} else if (prev) {
  console.log('\nNothing changed against the previous month.');
}
