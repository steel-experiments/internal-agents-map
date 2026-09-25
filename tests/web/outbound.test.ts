// ABOUTME: Checks the referral parameters that outbound links to company websites carry.
// ABOUTME: The catalog data keeps the plain homepage; only the rendered link changes.
import { describe, expect, it } from 'vitest';
import { loadCatalog } from '../../src/lib/catalog';
import { organizationMarkdown, organizationView } from '../../src/lib/organization-view';
import { outboundUrl } from '../../src/lib/outbound';

describe('outbound referral links', () => {
  it('adds the referral parameters and keeps the path and the existing query', () => {
    const url = new URL(outboundUrl('https://www.example.com/team?lang=en#top', 'organization-profile'));
    expect(url.origin + url.pathname).toBe('https://www.example.com/team');
    expect(url.hash).toBe('#top');
    expect(Object.fromEntries(url.searchParams)).toEqual({
      lang: 'en',
      utm_source: 'internal-agents.com',
      utm_medium: 'referral',
      utm_campaign: 'organization-profile',
    });
  });

  it('keeps a URL that already has campaign parameters', () => {
    const tagged = 'https://example.com/?utm_source=partner';
    expect(outboundUrl(tagged, 'organization-profile')).toBe(tagged);
  });

  it('tags the HTML website link and keeps the Markdown link plain', () => {
    const catalog = loadCatalog();
    const view = organizationView(catalog, 'airbnb');
    expect(view.websiteUrl).toBe(outboundUrl(view.homepage, 'organization-profile'));
    const markdown = organizationMarkdown(catalog, 'airbnb');
    expect(markdown).toContain(`(${view.homepage})`);
    expect(markdown).not.toContain('utm_');
  });
});
