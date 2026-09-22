#!/usr/bin/env node
// ABOUTME: Reads a Search Console queries export and finds the terms within reach of the catalog.
// ABOUTME: It separates brand searches, lists the untracked queries, and marks the striking-distance positions.
// Usage: node .claude/skills/seo/scripts/gsc-queries.mjs <search-console-queries-export.csv>
import { readFileSync } from 'node:fs';
import { loadConfig, monthStamp, writeSnapshot, latestSnapshot, log } from './_lib.mjs';
import { parseGscTable } from './gsc-perf.mjs';

const config = loadConfig();
const month = monthStamp();
const csvPath = process.argv[2];
if (!csvPath) {
  log('usage: node .claude/skills/seo/scripts/gsc-queries.mjs <search-console-queries-export.csv>');
  process.exit(1);
}

const rules = config.query_rules;
const brandRe = new RegExp(rules.brand_pattern, 'i');
const tracked = new Set([...config.tracked_keywords, ...config.rank_keywords].map((k) => k.toLowerCase()));

const rows = parseGscTable(readFileSync(csvPath, 'utf8'), { key: /quer|keyword|term/ }).map((r) => ({
  query: r.key.toLowerCase(),
  clicks: r.clicks,
  impressions: r.impressions,
  position: r.position,
  brand: brandRe.test(r.key),
}));

const total = (list) => list.reduce((s, r) => s + r.impressions, 0);
const brand = rows.filter((r) => r.brand);
const nonBrand = rows.filter((r) => !r.brand);

// Striking distance: the catalog is shown, but below the first results. A title or a
// description change on that page is the cheapest move on the site.
const striking = nonBrand
  .filter((r) => r.position >= rules.striking_min_position && r.position <= rules.striking_max_position && r.impressions >= rules.min_impressions)
  .sort((a, b) => b.impressions - a.impressions);

// Demand the scripts do not see: a query with impressions that config.json does not track.
const untracked = nonBrand
  .filter((r) => r.impressions >= rules.min_impressions && !tracked.has(r.query))
  .sort((a, b) => b.impressions - a.impressions);

const summary = {
  queries: rows.length,
  brandShare: total(rows) ? total(brand) / total(rows) : 0,
  brand: { queries: brand.length, impressions: total(brand), clicks: brand.reduce((s, r) => s + r.clicks, 0) },
  nonBrand: { queries: nonBrand.length, impressions: total(nonBrand), clicks: nonBrand.reduce((s, r) => s + r.clicks, 0) },
  striking: striking.slice(0, 40),
  untracked: untracked.slice(0, 40),
};
log(`wrote ${writeSnapshot(config, 'queries', month, summary)}`);

const pct = (v) => `${(v * 100).toFixed(1)}%`;
console.log(`\n# Queries, ${month} (${rows.length} queries, source: ${csvPath})`);
console.log(`\nBrand searches: ${brand.length} queries, ${summary.brand.impressions.toLocaleString('en-US')} impressions (${pct(summary.brandShare)} of the site), ${summary.brand.clicks} clicks`);
console.log(`Other searches: ${nonBrand.length} queries, ${summary.nonBrand.impressions.toLocaleString('en-US')} impressions, ${summary.nonBrand.clicks} clicks`);

console.log(`\nStriking distance (position ${rules.striking_min_position} to ${rules.striking_max_position}, ${rules.min_impressions} impressions or more):`);
if (!striking.length) console.log('  none');
for (const r of striking.slice(0, 25)) console.log(`  #${r.position.toFixed(1).padStart(5)}  ${String(r.impressions).padStart(6)} imp  ${String(r.clicks).padStart(4)} clicks  ${r.query}`);

console.log(`\nQueries with demand that config.json does not track:`);
if (!untracked.length) console.log('  none');
for (const r of untracked.slice(0, 25)) console.log(`  ${String(r.impressions).padStart(6)} imp  #${r.position.toFixed(1).padStart(5)}  ${r.query}`);

const prev = latestSnapshot(config, 'queries', month);
if (prev?.data) {
  const p = prev.data;
  console.log(`\nAgainst ${prev.month}: brand share ${pct(p.brandShare)} to ${pct(summary.brandShare)}, other searches ${p.nonBrand.impressions.toLocaleString('en-US')} to ${summary.nonBrand.impressions.toLocaleString('en-US')} impressions`);
  const was = new Set(p.striking.map((r) => r.query));
  const entered = striking.filter((r) => !was.has(r.query));
  if (entered.length) console.log(`  entered striking distance: ${entered.slice(0, 10).map((r) => r.query).join(', ')}`);
} else {
  console.log('\nThere is no earlier queries snapshot, so this run is the first measurement.');
}
