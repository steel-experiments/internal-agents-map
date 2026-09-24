// ABOUTME: Holds the text of the two guides: headings, paragraphs, list items, and links.
// ABOUTME: The HTML pages and their Markdown exports render the same values from here.

import { termLabel } from './labels';
import { SITE_NAME } from './metadata';
import { canonicalUrl, entryPath, guidePath, lessonsIndexPath } from './routes';

export const DEFINITIONS_TITLE = `What makes an agent internal? · ${SITE_NAME}`;
export const DEFINITIONS_HEADING = 'What makes an agent internal?';
export const DEFINITIONS_DESCRIPTION =
  'How organizations turn general-purpose models into agents for their own work. ' +
  'Explore workflow breadth, organizational adaptation, and practical agent terminology.';

export const METHODOLOGY_TITLE = `Methodology · ${SITE_NAME}`;
export const METHODOLOGY_HEADING = 'Methodology';
export const METHODOLOGY_DESCRIPTION =
  'How Internal Agents Map records sources, separates reported claims from interpretation, ' +
  'and handles uncertainty.';

export const LESSONS_TITLE = `Lessons · ${SITE_NAME}`;
export const LESSONS_HEADING = 'Lessons';
export const LESSONS_DESCRIPTION =
  'Short lessons on agent design. Each lesson connects an observation to reports from teams ' +
  'that build internal agents.';
export const LESSONS_LEDE = 'Short observations for people who build agents.';
/** The two halves of the introduction, around the link to the catalog. */
export const LESSONS_INTRO_BEFORE = 'Each lesson examines a design choice from the ';
export const LESSONS_INTRO_AFTER =
  '. Sources describe what teams report. Our observations explain what those reports may ' +
  'mean for other builders.';
export const LESSONS_CLOSING =
  'These lessons describe selected cases. They do not establish that one design works best ' +
  'for every team.';

export interface GuideLink {
  readonly label: string;
  readonly url: string;
}

/** The repository documents the Methodology guide sends a reader to. */
export const REPOSITORY_LINKS: readonly GuideLink[] = [
  {
    label: 'Data schema',
    url: 'https://github.com/steel-experiments/internal-agents-map/blob/main/data/schema.md',
  },
  {
    label: 'Lesson writing rules',
    url: 'https://github.com/steel-experiments/internal-agents-map/blob/main/docs/lessons-writing.md',
  },
  {
    label: 'Contribution guide',
    url: 'https://github.com/steel-experiments/internal-agents-map/blob/main/CONTRIBUTING.md',
  },
];

export interface ReferencePlacement {
  readonly id: string;
  readonly name: string;
  readonly category: string;
  readonly reason: string;
  readonly links: readonly GuideLink[];
}

/**
 * Products and categories shown for comparison on the Definitions chart.
 * They are not catalog entries: they describe a default, unadapted setup.
 */
export const REFERENCE_PLACEMENTS: readonly ReferencePlacement[] = [
  {
    id: 'deep-research',
    name: 'Deep research agent',
    category: 'Research workflow',
    reason:
      'A ready-made agent for one research workflow: finding sources, reasoning across them, ' +
      'and producing a documented report. OpenAI, Google, and Perplexity offer examples.',
    links: [
      { label: 'OpenAI deep research', url: 'https://openai.com/index/introducing-deep-research/' },
      {
        label: 'Gemini Deep Research',
        url: 'https://support.google.com/gemini/answer/15719111?hl=en',
      },
      {
        label: 'Perplexity Research',
        url: 'https://www.perplexity.ai/help-center/en/articles/10738684-what-is-research-mode',
      },
    ],
  },
  {
    id: 'ready-made-task',
    name: 'Codex / Claude Code / Devin',
    category: 'Software engineering agents',
    reason:
      'Ready-made agents that cover several software engineering workflows. Repository ' +
      'instructions, internal development tools, and company processes can move a deployment upward.',
    links: [
      { label: 'Codex overview', url: 'https://developers.openai.com/' },
      {
        label: 'Claude Code overview',
        url: 'https://docs.anthropic.com/en/docs/claude-code/getting-started',
      },
      { label: 'Devin overview', url: 'https://docs.devin.ai/get-started/devin-intro' },
    ],
  },
  {
    id: 'general-assistant',
    name: 'ChatGPT / Claude',
    category: 'Default setup · reference products',
    reason:
      'General-purpose assistants that span many kinds of work. Company knowledge, connected ' +
      'apps, and custom tools can move a deployment upward.',
    links: [
      { label: 'ChatGPT use cases', url: 'https://learn.chatgpt.com/use-cases' },
      {
        label: 'Claude enterprise search',
        url: 'https://support.claude.com/en/articles/12489464-use-enterprise-search',
      },
    ],
  },
];

/** The reference markers that belong in the ready-made focused-agent region. */
export const READY_REFERENCES = REFERENCE_PLACEMENTS.filter(
  (item) => item.id === 'deep-research' || item.id === 'ready-made-task',
);

/** The reference marker that belongs in the "general-purpose assistants" region. */
export const ASSISTANT_REFERENCES = REFERENCE_PLACEMENTS.filter(
  (item) => item.id === 'general-assistant',
);

/** One piece of a text block: plain words, bold words, or a link. */
export type Inline = string | InlineStrong | InlineLink;

export interface InlineStrong {
  readonly strong: string;
}

export interface InlineLink {
  readonly text: string;
  /** An address outside the website. */
  readonly href?: string;
  /** A path inside the website. The Markdown export makes it absolute. */
  readonly path?: string;
}

/** One text block, such as a paragraph or a caption. */
export type TextBlock = readonly Inline[];

/** A link from a guide header to a section of the same page. */
export interface JumpLink {
  readonly label: string;
  readonly fragment: string;
}

/** The address a link part uses inside a page. */
export function inlineHref(link: InlineLink): string {
  return link.href ?? link.path ?? '';
}

/** The Markdown form of one text block. */
export function inlineMarkdown(parts: TextBlock): string {
  return parts
    .map((part) => {
      if (typeof part === 'string') return part;
      if ('strong' in part) return `**${part.strong}**`;
      return `[${part.text}](${part.href ?? canonicalUrl(part.path ?? '')})`;
    })
    .join('');
}

/** The plain words of one text block, without bold marks or addresses. */
export function inlineText(parts: TextBlock): string {
  return parts
    .map((part) => (typeof part === 'string' ? part : 'strong' in part ? part.strong : part.text))
    .join('');
}

/** One part of the Methodology guide. */
export interface GuideSection {
  readonly id: string;
  /** The identifier of the heading, which labels the section. */
  readonly titleId: string;
  readonly heading: string;
  readonly body: readonly TextBlock[];
  /** The documents the section sends a reader to. */
  readonly links?: readonly GuideLink[];
}

export const METHODOLOGY_LEDE = 'How we record evidence and explain its limits.';

const CONTRIBUTING_URL =
  'https://github.com/steel-experiments/internal-agents-map/blob/main/CONTRIBUTING.md';

export const METHODOLOGY_SECTIONS: readonly GuideSection[] = [
  {
    id: 'methodology',
    titleId: 'inclusion-title',
    heading: 'What we include',
    body: [
      [
        'Each case describes a system that a named organization built or adapted for its own teams. Public sources must describe its implementation or use.',
      ],
      [
        'We maintain platforms and supporting tools in a separate Infrastructure collection, alongside the default Agents collection. A product name is optional. Commercial systems can qualify when sources describe the internal build or adaptation. General adoption claims are insufficient.',
      ],
    ],
  },
  {
    id: 'intake',
    titleId: 'intake-title',
    heading: 'How we add cases',
    body: [
      [
        'We use an agent skill to assess sources against our ',
        { text: 'inclusion rules', href: `${CONTRIBUTING_URL}#inclusion-rules` },
        ' and prepare catalog changes. Automated checks validate record structure, source files, and links; they cannot confirm reported results or our interpretations.',
      ],
    ],
  },
  {
    id: 'sources',
    titleId: 'sources-title',
    heading: 'How we use sources',
    body: [
      [
        'Claims link to public sources. We record who published each source and separate reported claims from our own judgments. We keep conflicting reports visible.',
      ],
      [
        'We capture a copy of each source page with ',
        {
          text: 'Steel, the open-source browser infrastructure for AI agents',
          href: 'https://steel.dev/',
        },
        '. Each capture records the time, the final URL, and the HTTP status. A capture shows what a page said when we read it. It does not confirm the claims on that page.',
      ],
      [
        'Company results remain self-reported unless an independent source verifies them. Confidence describes the support for a claim. Evidence strength describes source type and detail. Neither label proves that a claim is true.',
      ],
      [
        'For metrics, we keep the reported dates, scope, measurement method, and what the numbers count, when available. A report date does not establish the measurement period.',
      ],
      [
        'Unknown means that the sources do not provide an answer. It does not establish that a feature is absent.',
      ],
    ],
  },
  {
    id: 'levels',
    titleId: 'levels-title',
    heading: 'How we assign levels',
    body: [
      [
        'We assess specific tasks and when a person must review the work. Each level is our judgment, linked to evidence and a date. One system can have several levels for different tasks.',
      ],
      [
        'The levels do not rank companies or measure quality. See ',
        { text: 'the supervision definitions', path: `${guidePath('definitions')}#supervision` },
        ' for the terms and framework.',
      ],
    ],
  },
  {
    id: 'lessons',
    titleId: 'lessons-title',
    heading: 'How we write lessons',
    body: [
      [
        'We compare design choices across cases. Each ',
        { text: 'lesson', path: lessonsIndexPath() },
        ' links to its sources and separates what teams report from our observations.',
      ],
      [
        'We state the limits of each comparison. A repeated choice does not prove that it works better. Our illustrations explain the ideas and identify simplifications.',
      ],
    ],
  },
  {
    id: 'logos',
    titleId: 'logos-title',
    heading: 'How we use company logos',
    body: [
      ['Each logo is the trademark of its owner. The owner keeps all rights.'],
      [
        'The catalog shows a logo only to identify the organization of an entry. It does not show an endorsement, a partnership, or a review of the organization.',
      ],
      [
        'An owner can ask us to remove its logo. We then show a monogram instead. The entry itself does not change.',
      ],
      ['A logo says nothing about the evidence. It is not a quality signal.'],
    ],
  },
  {
    id: 'limits',
    titleId: 'limits-title',
    heading: 'What the map cannot tell you',
    body: [
      [
        'The map covers cases with public evidence. Many concern coding and code review. Failed projects and unpublished systems may be missing.',
      ],
      [
        'Case counts cannot tell us how common a practice is across the industry. Results from different tasks or measurement methods may not be comparable.',
      ],
    ],
    links: REPOSITORY_LINKS,
  },
];

/** A label above a value, such as a step of the workflow figure. */
export interface LabelledValue {
  readonly label: string;
  readonly value: string;
}

/** One end-to-end axis of the chart, from the first value to the last. */
export interface AxisScale {
  readonly from: string;
  readonly to: string;
}

/** One of the two questions the chart asks about an implementation. */
export interface ChartDimension {
  readonly heading: string;
  readonly description: TextBlock;
}

/** The heading of one region of the chart. */
export interface ChartCell {
  readonly scope: string;
  readonly title: string;
}

/** One picture of the terminology section, with its description. */
export interface ConceptFigure {
  /** The text a reader hears in place of the picture. */
  readonly label: string;
  readonly term: string;
  readonly caption: string;
}

/** One question and answer of the guide. */
export interface GuideQuestion {
  readonly question: string;
  readonly answer: TextBlock;
}

export interface ClassificationDefinition {
  readonly id: string;
  readonly label: string;
  readonly meaning: string;
}

export interface SupervisionDefinition extends ClassificationDefinition {
  readonly level: string;
  readonly attention: string;
}

const MINIONS_PATH = entryPath('stripe-minions');
const MINIONS_PART_ONE =
  'https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents';
const MINIONS_PART_TWO = `${MINIONS_PART_ONE}-part-2`;

export const DEFINITIONS_LEDE =
  'How organizations turn general-purpose models into agents for their own work.';

export const DEFINITIONS_INTRO: readonly TextBlock[] = [
  [
    'A model alone doesn’t know a company’s codebase, follow its processes, or have access to its tools. Organizations supply that context and access, and shape how the agent carries out work.',
  ],
  [
    'Internal Agents Map documents these systems: what they do, how teams build or adapt them, and what public evidence tells us about their use.',
  ],
];

export const DEFINITIONS_JUMP_LINKS: readonly JumpLink[] = [
  { label: 'Internal agents ↓', fragment: 'terms' },
  { label: 'How agents fit ↓', fragment: 'quadrant' },
  { label: 'Supervision ↓', fragment: 'supervision' },
  { label: 'Other terms ↓', fragment: 'terminology' },
];

export const WORK_DOMAIN_DESCRIPTION =
  'Work domain describes the kind of work an entry supports, such as coding, code review, support, or finance operations. One entry can cover several domains. This differs from workflow breadth, which describes how narrowly or broadly the system works.';

export const WORK_MODES_DESCRIPTION =
  'Work modes describe how work starts or proceeds. Interactive (foreground) and background describe participation; scheduled and event-driven describe triggers. One system can support several modes, such as event-driven background work.';

export const APPROACH_TYPE_DEFINITIONS: readonly ClassificationDefinition[] = [
  { id: 'agent', label: termLabel('agent'), meaning: 'One system that carries out tasks.' },
  { id: 'agent-system', label: termLabel('agent-system'), meaning: 'A documented family of independently useful agents; internal subagents alone do not establish a family.' },
  { id: 'platform', label: termLabel('platform'), meaning: 'Reusable infrastructure for several agents or workflows.' },
  { id: 'orchestration-system', label: termLabel('orchestration-system'), meaning: 'A system whose primary role is coordinating agents.' },
  { id: 'supporting-pattern', label: termLabel('supporting-pattern'), meaning: 'A narrower implemented component that enables agent operation.' },
];

export const INVOCATION_DEFINITIONS: readonly ClassificationDefinition[] = [
  { id: 'interactive', label: termLabel('interactive'), meaning: 'A person starts and exchanges messages with the system. This is foreground participation while those exchanges continue.' },
  { id: 'background', label: termLabel('background'), meaning: 'Work continues without continuous interaction after it starts.' },
  { id: 'scheduled', label: termLabel('scheduled'), meaning: 'A time rule starts the work.' },
  { id: 'event-driven', label: termLabel('event-driven'), meaning: 'A system event starts the work.' },
  { id: 'unknown', label: termLabel('unknown'), meaning: 'The collected evidence does not establish how work starts or proceeds.' },
];

export const SUPERVISION_DEFINITIONS = {
  heading: 'Supervision: where human attention returns',
  intro: [
    'The catalog assesses one documented workflow at a time. The boundary records when human attention normally returns during a successful run.',
  ] as TextBlock,
  source: [
    'Levels 2–5 adapt ',
    {
      text: "Dan Shapiro’s five levels of AI-assisted software development",
      href: 'https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/',
    },
    '. Levels 0–1 describe manual work and discrete assistance, outside the internal-agent workflows assessed here.',
  ] as TextBlock,
  rows: [
    { id: 'continuous-steering', label: termLabel('continuous-steering'), level: '2', attention: 'A person pairs with the agent throughout execution.', meaning: 'The person repeatedly guides the work as it proceeds.' },
    { id: 'work-product-review', label: termLabel('work-product-review'), level: '3', attention: 'A person reviews the draft or implementation.', meaning: 'The agent produces work, but review returns to the produced artifact.' },
    { id: 'outcome-review', label: termLabel('outcome-review'), level: '4', attention: 'A person evaluates tests, behavior, or outcomes.', meaning: 'The normal review boundary is the result rather than routine implementation inspection.' },
    { id: 'exception-only', label: termLabel('exception-only'), level: '5', attention: 'A person returns when the system raises an exception.', meaning: 'A normal successful run does not require routine human review.' },
    { id: 'unknown', label: termLabel('unknown'), level: '—', attention: 'Not established by the collected evidence.', meaning: 'The normal review boundary is undocumented or has not been assessed. Unknown does not mean no human supervision.' },
  ] as readonly SupervisionDefinition[],
  limits: [
    'Attention is separate from authority. A background run can still lack permission to publish, merge, spend money, or act in production. A level also does not state how long the system runs unattended.',
  ] as TextBlock,
  scope: [
    'A level describes the named workflow and evidence date. It does not rank a company, maturity, autonomy, or output quality. One system can therefore have several scoped levels.',
  ] as TextBlock,
} as const;

/** Section 01: what the map calls an internal agent. */
export const DEFINITIONS_SCOPE = {
  eyebrow: '01 / The scope of the map',
  heading: 'What is an internal agent?',
  definitionLabel: 'Working definition',
  definition: [
    'An ',
    { strong: 'internal agent' },
    ' works with company context and tools to carry out the organization’s own work.',
  ] as TextBlock,
  diagramLabel: 'An agent connected to knowledge, tools, and workflows within an organization',
  body: [
    [
      'It might investigate a failed deployment, prepare a code change, or help an employee resolve an IT issue. “Internal” describes the work it serves. The organization can build the system itself or adapt an existing product.',
    ],
    [
      'An agent answering customers directly serves a customer-facing role. One system can support both kinds of work.',
    ],
  ] as readonly TextBlock[],
  agentHeading: 'What makes it an agent?',
  agentBody: [
    [
      'For this guide, an ',
      { strong: 'agent' },
      ' uses a model to choose and carry out steps toward a task, using tools and feedback as it works.',
    ],
    [
      'Real systems often combine model-directed steps with programmed automation. A coding agent might decide how to fix a problem while a fixed pipeline runs tests and prepares the result for review.',
    ],
    ['The map separates task-performing Agents from the reusable Infrastructure that enables them. Lessons draw on both collections.'],
  ] as readonly TextBlock[],
} as const;

/** Section 02: one workflow, from the company task to the result. */
export const DEFINITIONS_WORKFLOW = {
  eyebrow: '02 / From a model to a workflow',
  heading: 'From a model to an internal workflow',
  intro: [
    'Consider ',
    { text: 'Stripe’s Minions', path: MINIONS_PATH },
    '. An engineer can ask a Minion to fix a flaky test. It works with Stripe’s code and development tools, makes a change, runs checks, and prepares a pull request for human review.',
  ] as TextBlock,
  steps: [
    { label: 'Company task', value: 'Fix a flaky test' },
    {
      label: 'Agent working with company context and tools',
      value: 'Stripe’s code · development environment · checks',
    },
    { label: 'Result in the company’s workflow', value: 'A pull request for human review' },
  ] as readonly LabelledValue[],
  caption: [
    'Sources: ',
    { text: 'Stripe’s workflow description', href: MINIONS_PART_ONE },
    ' and ',
    { text: 'execution environment', href: MINIONS_PART_TWO },
    '.',
  ] as TextBlock,
  closing: [
    'What makes this internal is its role in Stripe’s engineering work. Its cloud execution and unattended operation describe other aspects of the same system.',
  ] as TextBlock,
  catalogLink: {
    text: 'Explore Minions in the catalog',
    path: MINIONS_PATH,
  } as InlineLink,
} as const;

/** Section 03: the chart of work breadth and organizational adaptation. */
export const DEFINITIONS_CHART = {
  eyebrow: '03 / Different approaches',
  heading: 'How agents fit the organization',
  intro: ['Two questions help explain the different approaches in the map:'] as TextBlock,
  dimensions: [
    {
      heading: 'Horizontal axis indicates how broad the work is.',
      description: [
        'Focused agents follow one defined workflow. Broader agents perform many kinds of work. Shared platforms have a separate infrastructure index.',
      ],
    },
    {
      heading: 'Vertical axis defines how organization specific it is.',
      description: [
        'Standard products arrive with common capabilities. Internal systems add company knowledge, tools, conventions, and processes.',
      ],
    },
  ] as readonly ChartDimension[],
  legend: { catalog: 'Catalog entry', reference: 'Reference example' },
  verticalAxis: { from: 'Standard capabilities', to: 'Company-specific capabilities' },
  horizontalAxis: { from: 'One workflow', to: 'Many workflows' },
  cells: {
    specialized: { scope: 'Company-specific · focused', title: 'Specialized internal agents' },
    shared: {
      scope: 'Company-specific · broad',
      title: 'General internal agents',
    },
    ready: { scope: 'Standard · focused', title: 'Ready-made focused agents' },
    assistants: { scope: 'Standard · broad', title: 'General-purpose assistants' },
  } as Record<string, ChartCell>,
  emptyCell: 'No selected example currently fits.',
  caption: [
    'Illustrative placements based on public descriptions. Blue circles are agents; infrastructure is excluded from this comparison; green triangles are reference products or categories in their default setup. Positions show broad relationships, not measured scores. Spacing within a region is for readability.',
  ] as TextBlock,
  body: [
    [
      'The markers represent named systems and their documented scope. A company may operate several systems in different regions.',
    ],
    [
      'Broader scope and greater adaptation are not measures of quality. A focused agent may be exactly what a workflow needs.',
    ],
  ] as readonly TextBlock[],
  notesSummary: 'Why these systems are placed here',
  builtHeading: 'What the team built or adapted',
  builtBody: [
    [
      'An organization can adapt an existing product deeply, or build a small custom agent for a narrow task. Building software in-house does not by itself tell us how broadly the system works or how closely it fits the organization.',
    ],
    [
      'Each catalog entry looks at the concrete choices: context, tools, execution environment, workflow, and the parts the team built or configured.',
    ],
  ] as readonly TextBlock[],
} as const;

/** Section 04: the other words a reader meets, and what each one answers. */
export const DEFINITIONS_TERMS = {
  eyebrow: '04 / Other terms you’ll encounter',
  heading: 'Different questions about the same system',
  intro: ['These terms answer different questions about a system. They can apply together.'] as TextBlock,
  place: {
    heading: 'Cloud and local: where does the work run?',
    definition: ['Local and cloud describe ', { strong: 'where the agent runs.' }] as TextBlock,
    figures: [
      {
        label: 'Local execution: the agent runs inside your device',
        term: 'Local',
        caption: 'Execution on your device',
      },
      {
        label: 'Cloud execution: your device connects to an agent running on a remote computer',
        term: 'Cloud',
        caption: 'Execution on hosted infrastructure',
      },
    ] as readonly ConceptFigure[],
    body: [
      [
        'A ',
        { strong: 'cloud agent' },
        ' executes on hosted infrastructure, independently of the user’s device.',
      ],
      [
        'A ',
        { strong: 'local agent' },
        ' executes on the user’s device. It may still call a model hosted in the cloud: model hosting and agent execution can happen in different places.',
      ],
      [
        'Stripe’s Minions run on AWS EC2 development machines, making them an example of cloud execution.',
      ],
    ] as readonly TextBlock[],
  },
  participation: {
    heading: 'Foreground and background: how do people interact with it?',
    definition: [
      'Foreground and background describe ',
      { strong: 'how you participate while it works.' },
    ] as TextBlock,
    figures: [
      {
        label: 'Foreground work: repeated exchanges between you and the agent',
        term: 'Foreground',
        caption: 'Discuss, steer, and iterate as it works',
      },
      {
        label:
          'Background work: a trigger starts the agent, which works independently and returns a result',
        term: 'Background',
        caption: 'Work proceeds without continuous interaction',
      },
    ] as readonly ConceptFigure[],
    body: [
      [
        { strong: 'Foreground work' },
        ' involves active interaction with a person: discussing the task, giving instructions, or steering the next steps.',
      ],
      [
        { strong: 'Background work' },
        ' proceeds without continuous interaction. A person can start it and return later, or a schedule or event can trigger it.',
      ],
      [
        'These are modes of work. The same agent can move between them. An engineer might give a Minion instructions, leave it to work, then return to discuss the result.',
      ],
    ] as readonly TextBlock[],
  },
  combination: {
    label: 'These descriptions work together',
    lede: [
      'One agent can be ',
      { strong: 'internal, cloud-hosted, and background.' },
    ] as TextBlock,
    pairs: [
      { label: 'Whose work?', value: 'Internal' },
      { label: 'Where does it run?', value: 'Cloud' },
      { label: 'How do you participate?', value: 'Background' },
    ] as readonly LabelledValue[],
    note: 'A local agent can also work in the background. A cloud agent can work with you in the foreground.',
  },
  autonomy: {
    id: 'autonomy',
    heading: 'Autonomy: what can it do without approval?',
    body: [
      [
        { strong: 'Autonomy' },
        ' describes the decisions and actions an agent can take without human approval.',
      ],
    ] as readonly TextBlock[],
    lead: ['Describe that authority concretely:'] as TextBlock,
    quote:
      'A Minion can write code and run checks on its own. Production pull requests require human review.',
    closing: [
      'Working without someone’s continuous attention does not imply permission to take every action.',
    ] as TextBlock,
  },
} as const;

/** Section 05: the questions readers ask about the definitions. */
export const DEFINITIONS_QUESTIONS = {
  eyebrow: '05 / Common questions',
  heading: 'Common questions',
  items: [
    {
      question: 'Does “internal” mean built in-house?',
      answer: [
        'No. A company can configure an existing product around its own workflows. The relevant question is what work the system serves and how it uses company context and tools.',
      ],
    },
    {
      question: 'Does “internal” mean private or self-hosted?',
      answer: [
        'No. An internal agent can use hosted services. Hosting, data handling, and access controls need to be described separately.',
      ],
    },
    {
      question: 'Is a shared agent platform itself an agent?',
      answer: [
        'A platform can provide the context, tools, execution environments, and controls used by multiple agents. The Infrastructure collection preserves this architecture research without counting platforms as agents. The default Agents collection covers the systems that perform identifiable work.',
      ],
    },
    {
      question: 'Is every automated workflow an agent?',
      answer: [
        'For this guide, the distinction is whether a model chooses steps or actions as the task unfolds. A fixed sequence of programmed steps is automation; a system can combine both.',
      ],
    },
    {
      question: 'Why are some details unknown?',
      answer: [
        'Public descriptions vary in depth. An article may explain a workflow without documenting its permissions or execution environment. The map leaves those details unknown rather than inferring them from a product name.',
      ],
    },
    {
      question: 'Are these official definitions?',
      answer: [
        'These are working definitions for reading the map. Product terminology varies. Concrete descriptions of the work, context, tools, and behavior are more useful than a label alone.',
      ],
    },
  ] as readonly GuideQuestion[],
} as const;
