#!/usr/bin/env node
// ABOUTME: Phase 0 of the SEO pulse: reads a Search Console pages export into site and family totals.
// ABOUTME: It reports the site with and without the impression sinks, so the comparison holds each month.
// Usage: node .claude/skills/seo/scripts/gsc-perf.mjs <search-console-pages-export.csv>
import { loadConfig, familyOf, monthStamp, writeSnapshot, latestSnapshot, log } from './_lib.mjs';

/** Compare on the path only: an export can hold full URLs or bare paths. */
function normalizePath(page) {
  let path = String(page || '').trim();
  try { path = new URL(path).pathname; } catch { /* it is already a path */ }
  return path.length > 1 ? path.replace(/\/$/, '') : path;
}

function splitCsvLine(line) {
  const cells = [];
  let cell = '';
  let quoted = false;
  for (const ch of line) {
    if (ch === '"') quoted = !quoted;
    else if (ch === ',' && !quoted) { cells.push(cell); cell = ''; }
    else cell += ch;
  }
  cells.push(cell);
  return cells.map((c) => c.trim());
}

function toNumber(cell) {
  return Number(String(cell).replace(/[,%\s]/g, '')) || 0;
}

/**
 * Parse a Search Console export into rows of key, clicks, impressions, and position.
 * The column order and the name of the first column change between exports, so the headers
 * decide which column is which. `key` is the pattern of the first column: a page or a query.
 */
export function parseGscTable(text, { key }) {
  const lines = text.replace(/^\uFEFF/, '').split('\n').filter((l) => l.trim());
  if (!lines.length) return [];
  const headers = splitCsvLine(lines[0]).map((h) => h.toLowerCase());
  const col = (re) => headers.findIndex((h) => re.test(h));
  const keyCol = col(key);
  const clicksCol = col(/click/);
  const impressionsCol = col(/impression/);
  const positionCol = col(/position/);
  if (keyCol < 0 || clicksCol < 0 || impressionsCol < 0) {
    throw new Error(`the export has unexpected columns: ${headers.join(', ')}`);
  }
  return lines.slice(1).map((line) => {
    const cells = splitCsvLine(line);
    return {
      key: cells[keyCol],
      clicks: toNumber(cells[clicksCol]),
      impressions: toNumber(cells[impressionsCol]),
      position: positionCol >= 0 ? toNumber(cells[positionCol]) : null,
    };
  });
}

/** The pages export: one row for each page. */
export function parseGscCsv(text) {
  return parseGscTable(text, { key: /page|url|address/ }).map((r) => ({ page: r.key, clicks: r.clicks, impressions: r.impressions }));
}

function ratio(clicks, impressions) { return impressions ? clicks / impressions : 0; }

function totals(rows) {
  const clicks = rows.reduce((s, r) => s + r.clicks, 0);
  const impressions = rows.reduce((s, r) => s + r.impressions, 0);
  return { clicks, impressions, ctr: ratio(clicks, impressions) };
}

/**
 * The site totals, the same totals without the sink pages, each sink on its own, and
 * the totals of each route family. The families answer which template earns the traffic.
 */
export function summarize(config, rows, sinkPaths) {
  const sinkKeys = new Set(sinkPaths.map(normalizePath));
  const isSink = (row) => sinkKeys.has(normalizePath(row.page));
  const total = totals(rows);
  const sinks = sinkPaths.map((path) => {
    const matched = rows.filter((r) => normalizePath(r.page) === normalizePath(path));
    const t = totals(matched);
    return { path, ...t, impressionShare: ratio(t.impressions, total.impressions) };
  });
  const families = {};
  for (const row of rows) {
    if (isSink(row)) continue;
    const family = familyOf(config, normalizePath(row.page));
    families[family] ||= { clicks: 0, impressions: 0, pages: 0 };
    families[family].clicks += row.clicks;
    families[family].impressions += row.impressions;
    families[family].pages += 1;
  }
  for (const f of Object.values(families)) f.ctr = ratio(f.clicks, f.impressions);
  const exSinkRows = rows.filter((r) => !isSink(r));
  const top = [...exSinkRows].sort((a, b) => b.clicks - a.clicks).slice(0, 10)
    .map((r) => ({ path: normalizePath(r.page), ...r, ctr: ratio(r.clicks, r.impressions) }));
  const noClicks = exSinkRows.filter((r) => r.clicks === 0 && r.impressions >= 50).length;
  return { total, exSinks: totals(exSinkRows), sinks, families, top, pagesWithImpressionsAndNoClicks: noClicks };
}

function pct(value) { return `${(value * 100).toFixed(2)}%`; }
function line(label, t) {
  return `${label}: ${t.clicks} clicks, ${t.impressions.toLocaleString('en-US')} impressions, ${pct(t.ctr)} click-through`;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const csvPath = process.argv[2];
  if (!csvPath) {
    log('usage: node .claude/skills/seo/scripts/gsc-perf.mjs <search-console-pages-export.csv>');
    process.exit(1);
  }
  const config = loadConfig();
  const month = monthStamp();
  const { readFileSync } = await import('node:fs');
  const summary = summarize(config, parseGscCsv(readFileSync(csvPath, 'utf8')), config.impression_sinks);

  log(`wrote ${writeSnapshot(config, 'perf', month, summary)}`);

  console.log(`\n# Search performance, ${month} (source: ${csvPath})`);
  console.log(line('\nSite as exported', summary.total));
  console.log(line('Site without the sinks', summary.exSinks));
  if (summary.sinks.length) {
    console.log('\nImpression sinks, excluded from the second row (config.json, impression_sinks):');
    for (const s of summary.sinks) {
      console.log(`  ${s.path}: ${s.impressions.toLocaleString('en-US')} impressions (${pct(s.impressionShare)} of the site), ${s.clicks} clicks, ${pct(s.ctr)} click-through`);
    }
  } else {
    console.log('\nNo impression sinks are configured, so the two rows above are the same.');
  }

  console.log('\nBy route family:');
  for (const [family, t] of Object.entries(summary.families).sort((a, b) => b[1].impressions - a[1].impressions)) {
    console.log(`  ${family.padEnd(14)} ${String(t.pages).padStart(4)} pages  ${String(t.clicks).padStart(5)} clicks  ${t.impressions.toLocaleString('en-US').padStart(9)} impressions  ${pct(t.ctr)}`);
  }

  console.log('\nHighest clicks:');
  for (const r of summary.top) console.log(`  ${String(r.clicks).padStart(5)} clicks  ${pct(r.ctr).padStart(7)}  ${r.path}`);
  console.log(`\nPages with 50 impressions or more and no clicks: ${summary.pagesWithImpressionsAndNoClicks}`);

  const prev = latestSnapshot(config, 'perf', month);
  if (prev?.data?.exSinks) {
    console.log(`\n${line(`Against ${prev.month}, without the sinks`, prev.data.exSinks)}`);
  } else {
    console.log('\nThere is no earlier performance snapshot, so this run is the first measurement.');
  }
}
