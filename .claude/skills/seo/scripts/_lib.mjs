// ABOUTME: Shared helpers of the SEO pulse scripts: configuration, environment, and the DataForSEO client.
// ABOUTME: It also holds the snapshot store and the route families that every phase reports against.
import { readFileSync, writeFileSync, existsSync, readdirSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SKILL_DIR = join(dirname(fileURLToPath(import.meta.url)), '..');
export const REPO_ROOT = process.cwd();
export const CONFIG_PATH = join(SKILL_DIR, 'config.json');

export function loadConfig() {
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
}

/** Read the publication inventory the website build writes. */
export function loadRoutes(config) {
  const path = join(REPO_ROOT, config.paths.routing_manifest);
  if (!existsSync(path)) {
    throw new Error(`${config.paths.routing_manifest} is missing. Run "npm run build" from the repository root first.`);
  }
  const inventory = JSON.parse(readFileSync(path, 'utf8'));
  return Object.entries(inventory.routes).map(([route, files]) => ({ path: route, ...files }));
}

/** Name the family of a canonical path, or `other` when no pattern matches. */
export function familyOf(config, path) {
  const family = config.route_families.find((f) => new RegExp(f.pattern).test(path));
  return family ? family.id : 'other';
}

export function familyRules(config, id) {
  return config.route_families.find((f) => f.id === id) || null;
}

/** Walk up from the repository root to find the .env file that holds the credentials. */
export function loadEnv(start = REPO_ROOT) {
  let dir = start;
  for (let i = 0; i < 6; i++) {
    const p = join(dir, '.env');
    if (existsSync(p)) {
      for (const line of readFileSync(p, 'utf8').split('\n')) {
        const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
        if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
      }
      return p;
    }
    dir = dirname(dir);
  }
  return null;
}

export function authHeader() {
  loadEnv();
  const b64 = process.env.DATAFORSEO_AUTH;
  if (b64) return `Basic ${b64}`;
  if (process.env.DATAFORSEO_LOGIN && process.env.DATAFORSEO_PASSWORD) {
    return `Basic ${Buffer.from(`${process.env.DATAFORSEO_LOGIN}:${process.env.DATAFORSEO_PASSWORD}`).toString('base64')}`;
  }
  throw new Error('DataForSEO credentials are missing. Set DATAFORSEO_AUTH, or LOGIN and PASSWORD, in .env');
}

export const BASE = process.env.DATAFORSEO_BASE_URL || 'https://api.dataforseo.com';

/**
 * Call one DataForSEO endpoint. The payload becomes a task list of one.
 * The top-level status and the task status are both read: the service can answer 20000
 * at the top while the task itself failed, which would otherwise look like an empty result.
 */
export async function dfs(path, payload) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { Authorization: authHeader(), 'Content-Type': 'application/json' },
    body: JSON.stringify([payload]),
  });
  const json = await res.json();
  const top = json.status_code;
  const task = json.tasks?.[0]?.status_code;
  const taskMsg = json.tasks?.[0]?.status_message;
  if (top === 40104 || task === 40104) {
    throw new Error('The DataForSEO account is not verified (40104). Verify it at https://app.dataforseo.com/ and run again.');
  }
  if (top === 40200 || task === 40200) {
    throw new Error('The DataForSEO balance is empty (40200). Add credit at https://app.dataforseo.com/ and run again.');
  }
  if (top && top !== 20000) throw new Error(`DataForSEO ${path} -> top ${top} ${json.status_message}`);
  if (task && task !== 20000) throw new Error(`DataForSEO ${path} -> task ${task} ${taskMsg || ''}`.trim());
  return json;
}

export function monthStamp(d = new Date()) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
}

export function pulsePath(config, sub) {
  return join(REPO_ROOT, config.paths[sub]);
}

export function ensureDir(p) {
  mkdirSync(p, { recursive: true });
}

/** Write one snapshot as <name>-<month>.json. */
export function writeSnapshot(config, name, month, data) {
  const dir = pulsePath(config, 'snapshots_dir');
  ensureDir(dir);
  const path = join(dir, `${name}-${month}.json`);
  writeFileSync(path, JSON.stringify({ month, generatedAt: new Date().toISOString(), data }, null, 2));
  return path;
}

/** Return the most recent <name>-*.json snapshot older than `excludeMonth`. */
export function latestSnapshot(config, name, excludeMonth = null) {
  const dir = pulsePath(config, 'snapshots_dir');
  if (!existsSync(dir)) return null;
  const files = readdirSync(dir)
    .filter((f) => f.startsWith(`${name}-`) && f.endsWith('.json'))
    .filter((f) => !excludeMonth || !f.includes(`-${excludeMonth}.json`))
    .sort()
    .reverse();
  if (!files.length) return null;
  return JSON.parse(readFileSync(join(dir, files[0]), 'utf8'));
}

export function log(...a) { process.stderr.write(a.join(' ') + '\n'); }
