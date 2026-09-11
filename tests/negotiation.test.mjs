import { test } from 'node:test';
import assert from 'node:assert/strict';
import { wantsMarkdown } from '../scripts/negotiation.mjs';

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
