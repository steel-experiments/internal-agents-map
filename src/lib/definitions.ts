// ABOUTME: Places selected implementations on the Definitions chart from their claims.
// ABOUTME: A placement disappears when the evidence it names is no longer in the catalog.

import type { Catalog, Claim } from './catalog';
import { REFERENCE_PLACEMENTS, type ReferencePlacement } from './guide-content';
import { entryPath } from './routes';

/** The four regions of the chart. */
export type QuadrantCell = 'specialized' | 'shared' | 'ready' | 'assistants';

/**
 * A position on the whole plot, from 0 to 100 on each axis.
 * `x` runs from one workflow to many workflows; `y` runs from standard to company-specific.
 * A position is an editorial illustration, not a measured score.
 */
export interface ChartPosition {
  readonly x: number;
  readonly y: number;
}

/** The region follows from the position, so the two cannot disagree. */
export function regionOf(x: number, y: number): QuadrantCell {
  if (y > 50) return x < 50 ? 'specialized' : 'shared';
  return x < 50 ? 'ready' : 'assistants';
}

/** The fragment of the note that explains one marker. */
export function markerAnchor(id: string): string {
  return `placement-${id}`;
}

/** The claim a placement depends on, and the word the reader sees for it. */
export interface PlacementRequirement {
  readonly field: string;
  readonly label: string;
}

export interface PlacementCandidate extends ChartPosition {
  readonly id: string;
  /** The editorial reason for the position, shown in the placement notes. */
  readonly reason: string;
  readonly requirements: readonly PlacementRequirement[];
}

export interface PlacementEvidenceLink {
  readonly label: string;
  /** The claim anchor on the entry page of the implementation. */
  readonly href: string;
}

export interface PlacementView extends ChartPosition {
  readonly id: string;
  readonly path: string;
  readonly company: string;
  readonly agentName: string;
  readonly cell: QuadrantCell;
  readonly reason: string;
  readonly evidence: readonly PlacementEvidenceLink[];
}

/** The claims that support every placement, unless a candidate names other ones. */
const DEFAULT_REQUIREMENTS: readonly PlacementRequirement[] = [
  { field: 'summary', label: 'Scope' },
  { field: 'architecture.knowledge', label: 'Context' },
  { field: 'architecture.tool_access', label: 'Tools' },
];

/** Claim text that answers nothing. It cannot support a placement. */
const EMPTY_TEXT: ReadonlySet<string> = new Set(['', 'unknown', 'not specified']);

/**
 * The editorial placements of the Definitions chart.
 * These are scoped assessments of described work, not scores or rankings.
 */
export const PLACEMENT_CANDIDATES: readonly PlacementCandidate[] = [
  {
    id: 'doordash-code-review',
    x: 8,
    y: 82,
    reason: 'One code-review workflow, grounded in repository evidence and domain rules.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'stripe-minions',
    x: 44,
    y: 78,
    reason:
      'Several engineering tasks within a coding workflow, connected to Stripe’s development tools and repository rules. Placed toward the middle of workflow breadth.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'posthog-stamphog',
    x: 8,
    y: 72,
    reason:
      'One pull-request approval workflow, grounded in repository-specific safety gates, review state, ownership, and prior human approvals.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'ramp-inspect',
    x: 44,
    y: 70,
    reason:
      'A background coding agent that verifies work with tests, telemetry, feature flags, and the rendered frontend; it later expanded into production monitoring and a host for other internal agents.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'spotify-honk-xirp',
    x: 34,
    y: 84,
    reason:
      'A background coding agent on the Claude Agent SDK, adapted with Spotify’s own harness, trusted CI tools, and component ownership from Backstage. The arrow shows a standard coding agent moved upward.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'github-qubot',
    x: 12,
    y: 62,
    reason:
      'One data-analytics workflow on the GitHub Copilot cloud agent, grounded in a context layer that teams contribute to and in the company data warehouse. The arrow shows a coding agent moved upward into work that is not coding.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'meta-rea',
    x: 32,
    y: 63,
    reason:
      'One machine learning experimentation workflow for the ads ranking models, grounded in a database of past experiments and connected to Meta’s job schedulers and experiment tracking.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'sentry-junior',
    x: 78,
    y: 76,
    reason:
      'A general internal agent that takes varied tasks across company systems, with persistent context and tools discovered through MCP.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'salesforce-slackbot',
    x: 88,
    y: 84,
    reason:
      'An employee agent that finds company context, drafts work, and joins Slack context with Salesforce data. It is also a front door to other agents.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'sierra-pinecone',
    x: 64,
    y: 57,
    reason:
      'A shared interface for employee work that routes each request to a model, harness, and environment, and reaches 45 company systems through an MCP gateway.',
    requirements: DEFAULT_REQUIREMENTS,
  },
  {
    id: 'cursor-support-workflow',
    x: 34,
    y: 44,
    reason:
      'Cursor’s own product, configured for support investigations with workspaces over the product repositories and MCP servers for support systems. The team configured a standard product and did not build a new one, so it sits low, but above the default setup.',
    requirements: DEFAULT_REQUIREMENTS,
  },
];

/** A claim supports a placement when it says something and a source supports it. */
function supportsPlacement(claim: Claim | undefined): claim is Claim {
  if (!claim) return false;
  if (EMPTY_TEXT.has(String(claim.text).trim().toLowerCase())) return false;
  return claim.evidence.some((evidence) => evidence.relation === 'supports');
}

/**
 * Build the placements the chart can show.
 * A candidate is left out when any claim it names is missing or unsupported.
 */
export function placements(catalog: Catalog): PlacementView[] {
  const byId = new Map(PLACEMENT_CANDIDATES.map((candidate) => [candidate.id, candidate]));
  const claims = new Map(catalog.claims.map((claim) => [claim.id, claim]));
  const views: PlacementView[] = [];
  for (const approach of catalog.approaches.filter((item) => item.catalog_section === 'agents')) {
    const candidate = byId.get(approach.id);
    if (!candidate) continue;
    const evidence = new Map<string, Claim>();
    for (const claimId of approach.claim_ids) {
      const claim = claims.get(claimId);
      if (claim) evidence.set(claim.field, claim);
    }
    const supported = candidate.requirements.every((requirement) =>
      supportsPlacement(evidence.get(requirement.field)),
    );
    if (!supported) continue;
    views.push({
      id: approach.id,
      path: entryPath(approach.id),
      company: approach.company,
      agentName: approach.agent_name,
      x: candidate.x,
      y: candidate.y,
      cell: regionOf(candidate.x, candidate.y),
      reason: candidate.reason,
      evidence: candidate.requirements.map((requirement) => ({
        label: requirement.label,
        href: `${entryPath(approach.id)}#claim-${evidence.get(requirement.field)!.id}`,
      })),
    });
  }
  return views;
}

/** Group the placements by the region of the chart that holds them. */
export function placementsByCell(catalog: Catalog): Record<QuadrantCell, PlacementView[]> {
  const cells: Record<QuadrantCell, PlacementView[]> = {
    specialized: [],
    shared: [],
    ready: [],
    assistants: [],
  };
  for (const placement of placements(catalog)) cells[placement.cell].push(placement);
  return cells;
}

export interface ReferenceMarkerView extends ReferencePlacement {
  readonly cell: QuadrantCell;
}

/** The reference products and categories, each with the region its position gives. */
export function referenceMarkers(): ReferenceMarkerView[] {
  return REFERENCE_PLACEMENTS.map((item) => ({ ...item, cell: regionOf(item.x, item.y) }));
}

/** A reference product, and a catalog entry that a company built on it. */
export interface UpgradePath {
  readonly from: string;
  readonly to: string;
}

/**
 * The arrows that show a deployment moving upward: from a standard product to a
 * company-specific system built on it. Each target names its base product in its claims.
 */
export const UPGRADE_PATHS: readonly UpgradePath[] = [
  { from: 'ready-made-task', to: 'spotify-honk-xirp' },
  { from: 'ready-made-task', to: 'github-qubot' },
];

export interface UpgradePathView {
  readonly from: ChartPosition & { readonly id: string };
  readonly to: ChartPosition & { readonly id: string };
}

/** The arrows the chart can draw. An arrow goes when its catalog entry loses its placement. */
export function upgradePaths(catalog: Catalog): UpgradePathView[] {
  const references = new Map(REFERENCE_PLACEMENTS.map((item) => [item.id, item]));
  const placed = new Map(placements(catalog).map((item) => [item.id, item]));
  return UPGRADE_PATHS.flatMap((path) => {
    const from = references.get(path.from);
    const to = placed.get(path.to);
    if (!from || !to) return [];
    return [{ from: { id: from.id, x: from.x, y: from.y }, to: { id: to.id, x: to.x, y: to.y } }];
  });
}
