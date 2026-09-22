// ABOUTME: Turns catalog identifiers and field paths into short human labels.
// ABOUTME: It keeps the wording of the published catalog stable across pages.

const TERM_LABELS: Record<string, string> = {
  'agent-system': 'Agent family',
  'supporting-pattern': 'Component',
  'orchestration-system': 'Orchestration',
  'ci-triage': 'CI triage',
  'on-call': 'On-call',
  'event-driven': 'Event-driven',
  'work-product-review': 'Work-product review',
  'exception-only': 'Exception-only',
  // The review states read as one wording wherever the catalog shows them.
  unreported: 'Not reported',
};

/** Make a readable label from an identifier such as `work-product-review`. */
export function termLabel(value: string): string {
  const known = TERM_LABELS[value];
  if (known) return known;
  const words = value.replace(/[-_]/g, ' ');
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/** Name the kind of statement a claim field path holds. */
export function fieldLabel(field: string): string {
  if (field === 'summary') return 'Summary';
  if (field === 'headline_metric') return 'Headline claim';
  if (field === 'architecture.context_mgmt') return 'Context management';
  if (field.startsWith('architecture.')) return termLabel(field.slice('architecture.'.length));
  if (field.startsWith('primitives.')) return 'Supporting component';
  if (field.startsWith('key_metrics.')) return 'Key observation';
  if (field.startsWith('lessons_learned.')) return 'Lesson';
  if (field.startsWith('operating_models.')) return 'Operating model assessment';
  return termLabel(field);
}

/** Name a supervision level, which can be unknown for a supporting system. */
export function levelLabel(level: number | null): string {
  return level === null ? 'Level unknown' : `Level ${level}`;
}

/**
 * Every attention boundary the catalog assesses, with the level the build derives
 * from it. The `unknown` boundary has no level. The build validates the records
 * against the same scale, so a boundary no record carries is still a real value.
 */
export const BOUNDARY_LEVELS: Readonly<Record<string, number | null>> = {
  'continuous-steering': 2,
  'work-product-review': 3,
  'outcome-review': 4,
  'exception-only': 5,
  unknown: null,
};

const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
];

/**
 * Write a recorded date the way it reads aloud: `2025-10` as October 2025.
 * The catalog records a year, a month, or a day, and an unrecognised shape is
 * returned unchanged rather than guessed at.
 */
export function observedDate(value: string): string {
  const match = /^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$/.exec(value.trim());
  if (!match) return value;
  const [, year, month, day] = match;
  if (!month) return year!;
  const name = MONTHS[Number(month) - 1];
  if (!name) return value;
  return day ? `${Number(day)} ${name} ${year}` : `${name} ${year}`;
}
