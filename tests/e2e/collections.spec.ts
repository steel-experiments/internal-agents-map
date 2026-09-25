// ABOUTME: Collection browsing and infrastructure profiles remain usable without JavaScript.
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const catalog = JSON.parse(readFileSync(new URL('../../data/agents.json', import.meta.url), 'utf8'));
const count = (section: string) => catalog.approaches.filter((item: any) => item.catalog_section === section).length;
for (const [path, section] of [['/', 'agents'], ['/infrastructure', 'infrastructure']]) {
  test(`${path} initially lists only ${section}, with a visible cross-collection link`, async ({ page }) => {
    await page.goto(path!);
    await expect(page.locator('article.entry:visible')).toHaveCount(count(section!));
    await expect(page.locator(`article.entry[data-collection="${section === 'agents' ? 'infrastructure' : 'agents'}"]:visible`)).toHaveCount(0);
    const menu = page.locator('.nav-toggle');
    if (await menu.isVisible()) await menu.click();
    await expect(page.locator('.nav-links a[href="/infrastructure"]')).toBeVisible();
    await expect(page.locator('.nav-links a[href="/"]')).toBeVisible();
  });
}
test('infrastructure has architecture first, stable claims, no agent attention levels, and Markdown parity', async ({ page, request }) => {
  await page.goto('/agents/harvey-spectre');
  const headings = await page.locator('.entry-section > h2').allTextContents();
  expect(headings.indexOf('Capabilities and architecture')).toBeLessThan(headings.indexOf('Documented uses'));
  await expect(page.locator('.entry-header')).not.toContainText('Human involvement');
  await expect(page.locator('#human-involvement')).not.toContainText('Level ');
  await expect(page.locator('.notice')).toHaveCount(0);
  for (const item of catalog.claims.filter((item: any) => item.approach_id === 'harvey-spectre')) {
    await expect(page.locator(`#claim-${item.id}`)).toHaveCount(1);
  }
  const text = await (await request.get('/agents/harvey-spectre.md')).text();
  expect(text).toContain('## Capabilities and architecture');
  expect(text).not.toContain('- Autonomy:');
  expect((await request.get('/infrastructure.md')).status()).toBe(200);
});
test('the sidebar keeps the data files and the contribution form in their own group', async ({ page }) => {
  await page.goto('/');
  const menu = page.locator('.nav-toggle');
  if (await menu.isVisible()) await menu.click();
  const group = page.getByRole('group', { name: 'Data and contributions' });
  await expect(group.locator('a')).toHaveText(['Suggest an agent', 'Data guide', 'Download JSON', 'Repository']);
  await expect(group.locator('a.contribute-link')).toHaveAttribute('href', /\/issues\/new\?template=catalog-suggestion\.yml$/);
});
