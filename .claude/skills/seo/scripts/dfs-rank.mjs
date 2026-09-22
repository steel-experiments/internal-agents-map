#!/usr/bin/env node
// ABOUTME: Phase 2 of the SEO pulse: reads the Google position of internal-agents.com for the ownable terms.
// ABOUTME: It records the ranking page and the top three results, then reports the changes since last month.
// Usage: node .claude/skills/seo/scripts/dfs-rank.mjs [--limit 8]
// This phase spends DataForSEO credit, about $0.05 to $0.10 for each keyword.
import { loadConfig, dfs, monthStamp, writeSnapshot, latestSnapshot, familyOf, log } from './_lib.mjs';

const config = loadConfig();
const month = monthStamp();
const site = config.site;
const limit = process.argv.includes('--limit') ? parseInt(process.argv[process.argv.indexOf('--limit') + 1]) : null;
const pool = config.rank_keywords || config.tracked_keywords;
const keywords = limit ? pool.slice(0, limit) : pool;

function findRank(items) {
  const hit = items.find((it) => it.domain && (it.domain === site || it.domain.endsWith('.' + site)));
  return hit ? { rank: hit.rank_group, url: hit.url, title: hit.title } : null;
}

const rows = [];
let stopped = false;
for (const kw of keywords) {
  if (stopped) { rows.push({ keyword: kw, error: 'not read, the balance is empty' }); continue; }
  try {
    const j = await dfs('/v3/serp/google/organic/live/regular', {
      keyword: kw, location_code: config.location_code, language_code: config.language_code,
      device: 'desktop', depth: config.serp_depth,
    });
    const items = j.tasks?.[0]?.result?.[0]?.items ?? [];
    const organic = items.filter((it) => ['organic', 'featured_snippet'].includes(it.type));
    const hit = findRank(organic);
    const rec = { keyword: kw, rank: hit ? hit.rank : null, url: hit ? hit.url : null };
    // The page that ranks tells which template earns the position, so the report can name the family.
    // Google can list the legacy .html name of a page; the family is the same, but the report
    // must see the name, so the URL is kept as returned and only the family lookup strips it.
    if (hit) {
      try {
        const pathname = new URL(hit.url).pathname.replace(/\.html$/, '').replace(/^\/index$/, '/');
        rec.family = familyOf(config, pathname);
        rec.legacyName = /\.html$/.test(new URL(hit.url).pathname);
      } catch { rec.family = 'other'; }
    }
    rec.top3 = organic.slice(0, 3).map((it) => ({ domain: it.domain, title: it.title }));
    rows.push(rec);
    log(`ok  "${kw}" ${rec.rank ? `#${rec.rank} ${rec.family}` : 'not in the top ' + config.serp_depth}`);
  } catch (e) {
    const msg = String(e.message);
    if (msg.includes('40104')) { log('err the account is not verified (40104), stopping'); process.exit(3); }
    if (msg.includes('credentials are missing')) { log(`err ${msg}`); process.exit(3); }
    if (msg.includes('40200')) {
      log('err the DataForSEO balance is empty (40200). Add credit at app.dataforseo.com. The remaining keywords are not read.');
      stopped = true;
      rows.push({ keyword: kw, error: 'not read, the balance is empty (40200)' });
      continue;
    }
    log(`err "${kw}": ${msg}`);
    rows.push({ keyword: kw, error: msg });
  }
}

// A run that read nothing must not replace the baseline of the month.
if (rows.every((r) => r.error)) {
  console.error('No keyword was read, so no snapshot was written. Fix the credentials or the balance and run again.');
  process.exit(2);
}
// A limited run keeps its snapshot: it is the answer to an empty balance, not a smoke test.
// It is marked partial, so the report says that position tracking is incomplete.
const partial = Boolean(limit) || rows.some((r) => r.error);
if (partial) log(`this snapshot holds ${rows.filter((r) => !r.error).length} of ${pool.length} keywords, so the report must say that position tracking is incomplete`);
log(`wrote ${writeSnapshot(config, 'ranks', month, { partial, keywords: pool.length, rows })}`);

// --- the difference against the previous month ---
const prev = latestSnapshot(config, 'ranks', month);
const changes = [];
if (prev) {
  const prevRows = Array.isArray(prev.data) ? prev.data : prev.data?.rows || [];
  const prevMap = new Map(prevRows.map((r) => [r.keyword, r]));
  for (const r of rows) {
    if (r.error) continue;
    const p = prevMap.get(r.keyword);
    if (!p || p.error) continue;
    if (r.rank === p.rank) continue;
    if (p.rank == null) changes.push({ keyword: r.keyword, type: 'entered', from: null, to: r.rank, url: r.url });
    else if (r.rank == null) changes.push({ keyword: r.keyword, type: 'left', from: p.rank, to: null });
    else changes.push({ keyword: r.keyword, type: r.rank < p.rank ? 'improved' : 'declined', from: p.rank, to: r.rank, url: r.url });
  }
}

console.log(`\n# Positions, ${month} (${rows.length} keywords, previous: ${prev?.month || 'none'})`);
const ranked = rows.filter((r) => !r.error && r.rank != null).sort((a, b) => a.rank - b.rank);
console.log('\nIn the results:');
for (const r of ranked) console.log(`  #${String(r.rank).padStart(2)}  ${(r.family || 'other').padEnd(13)} ${r.keyword}\n      ${r.url}${r.legacyName ? '   (the legacy .html name, not the clean path)' : ''}`);
const absent = rows.filter((r) => !r.error && r.rank == null);
console.log(`\nNot in the top ${config.serp_depth}: ${absent.length} keywords`);
for (const r of absent) console.log(`  ${r.keyword} — top result: ${r.top3?.[0]?.domain || 'unknown'}`);
if (changes.length) {
  console.log(`\nChanges against ${prev.month}:`);
  for (const c of changes) console.log(`  ${c.type}: ${c.from ?? '—'} to ${c.to ?? '—'}  ${c.keyword}`);
} else if (prev) {
  console.log('\nNo position changed against the previous month.');
}
const failed = rows.filter((r) => r.error);
if (failed.length) console.log(`\n${failed.length} keywords were not read. The report must say that position tracking is incomplete.`);
