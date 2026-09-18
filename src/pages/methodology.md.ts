// ABOUTME: Serves the Methodology guide as Markdown, section by section.
// ABOUTME: It renders the same text, links, and qualifications as the page.
import type { APIRoute } from 'astro';
import {
  METHODOLOGY_HEADING,
  METHODOLOGY_LEDE,
  METHODOLOGY_SECTIONS,
  inlineMarkdown,
} from '../lib/guide-content';
import { canonicalUrl, guidePath } from '../lib/routes';

function document(): string {
  const blocks: string[] = [
    `Source: ${canonicalUrl(guidePath('methodology'))}`,
    `# ${METHODOLOGY_HEADING}`,
    METHODOLOGY_LEDE,
  ];
  for (const section of METHODOLOGY_SECTIONS) {
    blocks.push(`## ${section.heading}`);
    for (const block of section.body) blocks.push(inlineMarkdown(block));
    if (section.links) {
      blocks.push(section.links.map((link) => `[${link.label}](${link.url})`).join(' '));
    }
  }
  return blocks.join('\n\n');
}

export const GET: APIRoute = () =>
  new Response(`${document()}\n`, {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
