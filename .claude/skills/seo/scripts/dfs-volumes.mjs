#!/usr/bin/env node
// ABOUTME: Phase 1 of the SEO pulse: refreshes search volume, cost per click, and the 12-month trend.
// ABOUTME: It writes a dated snapshot of the tracked keywords and reports the movers against last month.
// Usage: node .claude/skills/seo/scripts/dfs-volumes.mjs [--limit 10]
import { loadConfig, dfs, monthStamp, writeSnapshot, latestSnapshot, pulsePath, log, ensureDir } from './_lib.mjs';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

const config = loadConfig();
const month = monthStamp();
const limit = process.argv.includes('--limit') ? parseInt(process.argv[process.argv.indexOf('--limit') + 1]) : null;
const keywords = limit ? config.tracked_keywords.slice(0, limit) : config.tracked_keywords;

async function pullBatch(batch) {
  const j = await dfs('/v3/keywords_data/google_ads/search_volume/live', {
    keywords: batch,
    location_code: config.location_code,
    language_code: config.language_code,
  });
  return (j.tasks?.[0]?.result ?? []).map((r) => ({
    keyword: r.keyword,
    volume: r.search_volume ?? null,
    cpc: r.cpc ?? null,
    paid_competition: r.competition ?? null,
    competition_index: r.competition_index ?? null,
    trend: (r.monthly_searches ?? []).map((m) => `${m.year}-${String(m.month).padStart(2, '0')}:${m.search_volume}`),
  }));
}

const rows = [];
let stopped = false;
for (let i = 0; i < keywords.length; i += 25) {
  if (stopped) break;
  const batch = keywords.slice(i, i + 25);
  try {
    rows.push(...(await pullBatch(batch)));
    log(`ok  volumes batch ${Math.floor(i / 25) + 1} (${batch.length} keywords)`);
  } catch (e) {
    const msg = String(e.message);
    log(`err volumes batch: ${msg}`);
    if (msg.includes('40104') || msg.includes('40200') || msg.includes('credentials are missing')) {
      console.error(`\nSTOP: ${msg} ${keywords.length - rows.length} keywords were not read this month.`);
      stopped = true;
    }
  }
}

// A run that read nothing must not become the baseline of the month: the next run would
// compare against an empty set and report every keyword as new.
if (!rows.length) {
  console.error('No keyword was read, so no snapshot was written. Fix the credentials or the balance and run again.');
  process.exit(2);
}

const byKw = new Map(rows.map((r) => [r.keyword.toLowerCase(), r]));
// A keyword with no advertiser data stays in the set. Null is below the reporting threshold, not zero demand.
for (const k of keywords) {
  if (!byKw.has(k.toLowerCase())) {
    byKw.set(k.toLowerCase(), { keyword: k, volume: null, cpc: null, paid_competition: null, trend: [] });
  }
}

// A limited run is a check that the credentials work, not a measurement. It must not become
// the baseline of the month: next month would compare the full set against a handful of terms
// and report nothing for the rest.
if (limit) log(`this run holds ${limit} keywords, so it does not write the snapshot of the month`);
else log(`wrote ${writeSnapshot(config, 'volumes', month, [...byKw.values()])}`);

// --- the difference against the previous month ---
const prev = latestSnapshot(config, 'volumes', month);
const movers = [];
if (prev) {
  const prevMap = new Map((prev.data || []).map((r) => [r.keyword.toLowerCase(), r]));
  for (const r of byKw.values()) {
    const p = prevMap.get(r.keyword.toLowerCase());
    if (!p) continue;
    const dVol = (r.volume ?? 0) - (p.volume ?? 0);
    // The trend slope compares the average of the last three months with the three before them.
    const nums = (r.trend || []).map((t) => parseInt(t.split(':')[1])).filter((n) => !Number.isNaN(n));
    const recent = nums.slice(0, 3), older = nums.slice(3, 6);
    const recAvg = recent.length ? recent.reduce((a, b) => a + b, 0) / recent.length : 0;
    const oldAvg = older.length ? older.reduce((a, b) => a + b, 0) / older.length : 0;
    const slopePct = oldAvg > 0 ? Math.round(((recAvg - oldAvg) / oldAvg) * 100) : null;
    if (Math.abs(dVol) >= 50 || (slopePct !== null && Math.abs(slopePct) >= 25)) {
      movers.push({ keyword: r.keyword, prevVol: p.volume, vol: r.volume, dVol, slopePct });
    }
  }
  movers.sort((a, b) => Math.abs(b.dVol || 0) + Math.abs(b.slopePct || 0) - (Math.abs(a.dVol || 0) + Math.abs(a.slopePct || 0)));
}

ensureDir(pulsePath(config, 'pulse_dir'));
writeFileSync(
  join(pulsePath(config, 'pulse_dir'), `movers-${month}.json`),
  JSON.stringify({ month, previousMonth: prev?.month || null, movers }, null, 2),
);

console.log(`\n# Volumes, ${month} (${rows.length} keywords, previous: ${prev?.month || 'none'})`);
const sorted = [...byKw.values()].filter((r) => r.volume != null).sort((a, b) => (b.volume || 0) - (a.volume || 0));
console.log('\nHighest volume:');
for (const r of sorted.slice(0, 20)) console.log(`  ${String(r.volume).padStart(7)}  $${(r.cpc || 0).toFixed(2).padStart(7)}  ${r.keyword}`);
if (movers.length) {
  console.log(`\nMovers against ${prev.month} (volume change 50 or more, or trend change 25% or more):`);
  for (const m of movers.slice(0, 25)) {
    console.log(`  ${m.keyword}: ${m.prevVol} to ${m.vol} (${m.dVol >= 0 ? '+' : ''}${m.dVol})${m.slopePct !== null ? `, trend ${m.slopePct >= 0 ? '+' : ''}${m.slopePct}%` : ''}`);
  }
} else if (prev) {
  console.log('\nNo keyword moved enough to report against the previous month.');
}
