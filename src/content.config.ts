// ABOUTME: Declares the lessons collection and the metadata every lesson must carry.
// ABOUTME: The schema stops the build when a lesson is missing a required field.

import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** A calendar date, written as `YYYY-MM-DD` and kept as text. */
const isoDate = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}$/, 'the date must be written as YYYY-MM-DD.');

/** One numbered source at the end of a lesson. Its identifier is its anchor. */
const lessonSource = z.object({
  /** The anchor part of `#source-<id>` inside the lesson. */
  id: z.string().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/),
  title: z.string(),
  url: z.string().url(),
  /** What the lesson takes from that source. */
  note: z.string(),
});

const lessons = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/lessons' }),
  schema: z.object({
    title: z.string(),
    /** The page description, used for search results and link previews. */
    description: z.string(),
    /** The short label above the title, such as `01 / Run limits`. */
    eyebrow: z.string(),
    /** The opening line under the title. */
    lede: z.string(),
    /** The text the lessons index shows for this lesson. */
    summary: z.string(),
    /** The reading time the lesson reports, such as `2 min read`. */
    readingTime: z.string(),
    /** The position of the lesson in the reading order, counted from 1. */
    order: z.number().int().positive(),
    publishedAt: isoDate,
    /** The date of a later content change. Write it only when one happened. */
    updatedAt: isoDate.optional(),
    /** The catalog implementations this lesson examines. */
    relatedAgentIds: z.array(z.string()).nonempty(),
    sources: z.array(lessonSource).nonempty(),
  }),
});

export const collections = { lessons };
