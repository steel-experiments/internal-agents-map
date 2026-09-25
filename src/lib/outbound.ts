// ABOUTME: Adds referral parameters to outbound links so that the destination can see the catalog as the source.
// ABOUTME: Only rendered HTML links use it; citations and Markdown exports keep the URL as recorded.

/** The value of utm_source on each outbound link. */
export const REFERRAL_SOURCE = 'internal-agents.com';

/**
 * Return the URL with utm_source, utm_medium and utm_campaign.
 * A URL that already has a campaign parameter is returned as it is.
 */
export function outboundUrl(href: string, campaign: string): string {
  const url = new URL(href);
  if ([...url.searchParams.keys()].some((key) => key.startsWith('utm_'))) return href;
  url.searchParams.set('utm_source', REFERRAL_SOURCE);
  url.searchParams.set('utm_medium', 'referral');
  url.searchParams.set('utm_campaign', campaign);
  return url.toString();
}
