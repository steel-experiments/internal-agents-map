// ABOUTME: Tests for the edge routing rules: alias hosts, clean URLs, and Markdown negotiation.
// ABOUTME: It uses a fixture routing manifest in the shape that the site build writes.
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { CANONICAL_ORIGIN, matches, resolveRequest, wantsMarkdown } from '../scripts/negotiation.mjs';

const fixture = new URL('./fixtures/routing/routing-manifest.json', import.meta.url);
const { routes } = JSON.parse(readFileSync(fixture, 'utf8'));

/** Resolve one request against the fixture manifest. */
function resolve(path, { host = 'internal-agents.com', method = 'GET', accept = '' } = {}) {
  return resolveRequest({ routes, url: new URL(`https://${host}${path}`), method, accept });
}

const MARKDOWN = 'text/markdown';

test('browser defaults and wildcards remain HTML', () => {
  for (const accept of ['', '*/*', 'text/*', 'text/html,application/xhtml+xml,*/*;q=0.8']) {
    assert.equal(wantsMarkdown(accept), false, accept);
  }
});

test('explicit Markdown and quality preferences are respected', () => {
  for (const accept of ['text/markdown', 'TEXT/MARKDOWN; charset=utf-8', 'text/markdown,*/*', 'text/markdown;q=0.8,text/html;q=0.2', 'text/markdown,text/html;q=0']) {
    assert.equal(wantsMarkdown(accept), true, accept);
  }
  for (const accept of ['text/markdown;q=0', 'text/markdown;q=0,*/*', 'text/markdown;q=0.3,text/html', 'text/markdown,text/html', 'text/markdown;q=bad', 'text/markdown;q=2']) {
    assert.equal(wantsMarkdown(accept), false, accept);
  }
});

test('quality weights decide the representation of a known route', () => {
  for (const accept of ['text/markdown', 'text/markdown;q=0.8,text/html;q=0.2', 'text/markdown,*/*']) {
    assert.equal(resolve('/agents/uber-ureview', { accept }).type, 'markdown', accept);
  }
  for (const accept of ['', '*/*', 'text/markdown;q=0', 'text/markdown;q=0.3,text/html']) {
    assert.equal(resolve('/agents/uber-ureview', { accept }).type, 'pass', accept);
  }
});

test('alias hosts redirect to the canonical origin with path and query', () => {
  for (const host of ['www.internal-agents.com', 'internal-agents-map.vercel.app']) {
    assert.deepEqual(resolve('/lessons?x=1', { host }), {
      type: 'redirect',
      status: 308,
      location: 'https://internal-agents.com/lessons?x=1',
    });
  }
  assert.equal(resolve('/', { host: 'www.internal-agents.com' }).location, 'https://internal-agents.com/');
});

test('preview hosts and the canonical host are served without a host redirect', () => {
  assert.equal(resolve('/', { host: 'preview-abc-nen-labs.vercel.app' }).type, 'pass');
  assert.equal(resolve('/', { host: 'internal-agents.com' }).type, 'pass');
});

test('an alias host and a legacy path produce one redirect, not a chain', () => {
  assert.equal(
    resolve('/lessons/stop-a-run.html?x=1', { host: 'www.internal-agents.com' }).location,
    'https://internal-agents.com/lessons/stop-a-run?x=1',
  );
  assert.equal(
    resolve('/index.html', { host: 'internal-agents-map.vercel.app' }).location,
    'https://internal-agents.com/',
  );
});

test('legacy .html paths redirect to the clean route and keep the query', () => {
  for (const [request, location] of [
    ['/agents/block-builderbot.html', '/agents/block-builderbot'],
    ['/lessons.html?q=stripe', '/lessons?q=stripe'],
    ['/definitions.html', '/definitions'],
    ['/index.html?q=stripe', '/?q=stripe'],
  ]) {
    const decision = resolve(request);
    assert.equal(decision.type, 'redirect', request);
    assert.equal(decision.status, 308, request);
    assert.equal(decision.location, CANONICAL_ORIGIN + location, request);
  }
});

test('trailing slash variants redirect to the clean route', () => {
  assert.equal(resolve('/agents/block-builderbot/').location, CANONICAL_ORIGIN + '/agents/block-builderbot');
  assert.equal(resolve('/lessons/stop-a-run.html/').location, CANONICAL_ORIGIN + '/lessons/stop-a-run');
  assert.equal(resolve('/').type, 'pass');
});

test('entry and lesson routes return their Markdown export', () => {
  for (const [path, markdown] of [
    ['/agents/block-builderbot', '/agents/block-builderbot.md'],
    ['/lessons/stop-a-run', '/lessons/stop-a-run.md'],
    ['/', '/index.md'],
  ]) {
    const decision = resolve(path + '?q=stripe', { accept: MARKDOWN });
    assert.equal(decision.type, 'markdown', path);
    assert.equal(decision.path, markdown, path);
    assert.equal(decision.headers['Content-Type'], 'text/markdown; charset=utf-8');
    assert.equal(decision.headers.Vary, 'Accept');
    assert.equal(decision.headers['Cache-Control'], 'public, max-age=0, must-revalidate');
    assert.equal(decision.headers.Link, `<${CANONICAL_ORIGIN}${path}>; rel="canonical"`);
  }
});

test('an HTML page advertises its Markdown alternate and varies on Accept', () => {
  const decision = resolve('/agents/uber-ureview', { accept: 'text/html' });
  assert.equal(decision.type, 'pass');
  assert.equal(decision.headers.Vary, 'Accept');
  assert.match(decision.headers.Link, /^<https:\/\/internal-agents\.com\/agents\/uber-ureview\.md>; rel="alternate"; type="text\/markdown", /);
  assert.match(decision.headers.Link, /rel="collection"/);
});

test('a direct Markdown request gets the canonical link to its page', () => {
  assert.deepEqual(resolve('/agents/block-builderbot.md'), {
    type: 'pass',
    headers: { Link: `<${CANONICAL_ORIGIN}/agents/block-builderbot>; rel="canonical"` },
  });
  assert.deepEqual(resolve('/index.md'), {
    type: 'pass',
    headers: { Link: `<${CANONICAL_ORIGIN}/>; rel="canonical"` },
  });
  // An export without an HTML page keeps the headers of the host.
  assert.deepEqual(resolve('/data-guide.md'), { type: 'pass' });
});

test('methods other than GET and HEAD pass through', () => {
  assert.deepEqual(resolve('/agents/block-builderbot', { method: 'POST', accept: MARKDOWN }), { type: 'pass' });
  assert.equal(resolve('/agents/block-builderbot', { method: 'HEAD', accept: MARKDOWN }).type, 'markdown');
});

test('unknown paths and asset paths are untouched', () => {
  for (const path of ['/agents/does-not-exist', '/missing/nested/page.html', '/agents/index.json', '/_astro/index.Ab12Cd.js', '/assets/site.74648cb2.css', '/favicon.ico', '/robots.txt']) {
    assert.deepEqual(resolve(path), { type: 'pass' }, path);
  }
  for (const path of ['/_astro/index.Ab12Cd.js', '/assets/site.css', '/agents/index.json', '/sitemap.xml']) {
    assert.equal(matches(path), false, path);
  }
  for (const path of ['/', '/agents/block-builderbot', '/lessons/stop-a-run.html', '/index.md']) {
    assert.equal(matches(path), true, path);
  }
});

test('paths that look malicious never redirect off the canonical origin', () => {
  const paths = ['//evil.example', '/%2F%2Fevil.example', '//evil.example/index.html', '/https://evil.example', '/..//evil.example', '/lessons/stop-a-run.html/../../evil.example'];
  for (const path of paths) {
    for (const host of ['internal-agents.com', 'www.internal-agents.com']) {
      const decision = resolve(path, { host });
      if (decision.type === 'redirect') {
        assert.equal(new URL(decision.location).origin, CANONICAL_ORIGIN, path);
      } else {
        assert.deepEqual(decision, { type: 'pass' }, path);
      }
    }
  }
  // A file name that the matcher accepts still resolves against the canonical origin only.
  assert.equal(
    resolve('//evil.example/index.html', { host: 'www.internal-agents.com' }).location,
    'https://internal-agents.com//evil.example/index.html',
  );
});
