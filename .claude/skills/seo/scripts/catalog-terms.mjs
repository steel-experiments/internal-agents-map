#!/usr/bin/env node
// ABOUTME: Lists the search terms the catalog itself creates: one organization plus one system name for each record.
// ABOUTME: It marks which of them config.json tracks, so the keyword set follows the catalog as records arrive.
// Usage: node .claude/skills/seo/scripts/catalog-terms.mjs [--untracked]
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { loadConfig, REPO_ROOT } from './_lib.mjs';

const config = loadConfig();
const untrackedOnly = process.argv.includes('--untracked');
const catalog = JSON.parse(readFileSync(join(REPO_ROOT, 'data/agents.json'), 'utf8'));

/**
 * Turn a record into the term a person would type. A parenthesis holds an alias or a
 * qualifier, a slash joins several names, and a generic name such as "Internal coding
 * agent" says nothing without the organization, so the term keeps the organization first.
 */
function termsOf(record) {
  const company = record.company.toLowerCase();
  const names = record.agent_name
    .replace(/\(.*?\)/g, ' ')
    .split('/')
    .map((n) => n.trim().toLowerCase())
    .filter(Boolean);
  return names.map((name) => (name.startsWith(company) ? name : `${company} ${name}`).replace(/\s+/g, ' '));
}

// A term counts as tracked when a tracked keyword holds it or it holds one: "coinbase forge ai"
// tracks the Forge record, and "notion scruff" tracks "notion scruff".
const tracked = [...config.tracked_keywords, ...config.rank_keywords].map((k) => k.toLowerCase());
const isTracked = (term) => tracked.some((k) => k.includes(term) || term.includes(k));
const rows = catalog.approaches.map((record) => {
  const terms = termsOf(record);
  return { id: record.id, type: record.approach_type, terms, tracked: terms.some(isTracked) };
});

const shown = untrackedOnly ? rows.filter((r) => !r.tracked) : rows;
console.log(`# Catalog terms (${rows.filter((r) => r.tracked).length} of ${rows.length} records tracked)\n`);
for (const r of shown) {
  console.log(`${r.tracked ? 'tracked  ' : 'untracked'}  ${r.type.padEnd(18)} ${r.terms.join(' | ')}    (/agents/${r.id})`);
}
console.log('\nA generic name ("internal coding agent") is not a term anyone searches: skip it, or track the organization with "ai agents".');
