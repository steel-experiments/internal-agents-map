// ABOUTME: Lists the allowed values of each enum definition in data/agent.schema.json.
// ABOUTME: scripts/build.py generates this file. Do not edit it by hand.

export const APPROACH_TYPE_VALUES = ['agent', 'agent-system', 'platform', 'orchestration-system', 'supporting-pattern'] as const;
export type ApproachType = (typeof APPROACH_TYPE_VALUES)[number];

export const DEPLOYMENT_STAGE_VALUES = ['research', 'prototype', 'pilot', 'deployed', 'scaled', 'unknown'] as const;
export type DeploymentStage = (typeof DEPLOYMENT_STAGE_VALUES)[number];

export const STATUS_VALUES = ['internal', 'open-sourced', 'commercialized', 'mixed'] as const;
export type Status = (typeof STATUS_VALUES)[number];

export const DOMAIN_VALUES = ['coding', 'code-review', 'support', 'on-call', 'research', 'customer-success', 'security', 'finance-ops', 'data', 'ci-triage', 'maintenance', 'ops', 'recruitment', 'migrations', 'design'] as const;
export type Domain = (typeof DOMAIN_VALUES)[number];

export const AUTONOMY_VALUES = ['assistive', 'human-in-loop', 'drafts-reviewed', 'autonomous', 'unknown'] as const;
export type Autonomy = (typeof AUTONOMY_VALUES)[number];

export const ATTENTION_BOUNDARY_VALUES = ['continuous-steering', 'work-product-review', 'outcome-review', 'exception-only', 'unknown'] as const;
export type AttentionBoundary = (typeof ATTENTION_BOUNDARY_VALUES)[number];

export const INVOCATION_VALUES = ['interactive', 'background', 'scheduled', 'event-driven', 'unknown'] as const;
export type Invocation = (typeof INVOCATION_VALUES)[number];

export const RUBRIC_STATE_VALUES = ['run-only', 'durable-session', 'cross-session-memory', 'mixed', 'unknown'] as const;
export type RubricState = (typeof RUBRIC_STATE_VALUES)[number];

export const IDENTITY_VALUES = ['user', 'dedicated-agent', 'service', 'mixed', 'unknown'] as const;
export type Identity = (typeof IDENTITY_VALUES)[number];

export const EVIDENCE_STRENGTH_VALUES = ['detailed-primary', 'limited-primary', 'secondary-only', 'mixed', 'unknown'] as const;
export type EvidenceStrength = (typeof EVIDENCE_STRENGTH_VALUES)[number];

export const INTERFACE_VALUES = ['slack', 'github', 'web', 'cli', 'linear', 'chrome-extension', 'webhook', 'desktop', 'scheduled', 'skill', 'cursor', 'api', 'automation', 'ci', 'intercom', 'jira', 'internal-ui', 'mobile', 'monday'] as const;
export type Interface = (typeof INTERFACE_VALUES)[number];

export const RELATION_TYPE_VALUES = ['component-of', 'built-on', 'successor-of', 'related-to'] as const;
export type RelationType = (typeof RELATION_TYPE_VALUES)[number];

export const SOURCE_KIND_VALUES = ['engineering-blog', 'corporate-article', 'documentation', 'source-code', 'repository', 'release', 'social-post', 'talk', 'transcript', 'podcast', 'paper', 'case-study', 'news', 'hn-thread', 'hn-comment', 'forum', 'other'] as const;
export type SourceKind = (typeof SOURCE_KIND_VALUES)[number];

export const PROVENANCE_CLASS_VALUES = ['first-party', 'direct-participant', 'independent-secondary', 'community', 'aggregator'] as const;
export type ProvenanceClass = (typeof PROVENANCE_CLASS_VALUES)[number];

export const SOURCE_ROLE_VALUES = ['evidence', 'commentary', 'discovery'] as const;
export type SourceRole = (typeof SOURCE_ROLE_VALUES)[number];

export const EVIDENCE_RELATION_VALUES = ['supports', 'contradicts', 'contextualizes'] as const;
export type EvidenceRelation = (typeof EVIDENCE_RELATION_VALUES)[number];

export const CLAIM_KIND_VALUES = ['fact', 'metric', 'inference', 'opinion'] as const;
export type ClaimKind = (typeof CLAIM_KIND_VALUES)[number];

export const CLAIM_PROVENANCE_VALUES = ['reported', 'observed', 'inferred', 'catalog-judgment'] as const;
export type ClaimProvenance = (typeof CLAIM_PROVENANCE_VALUES)[number];

export const CONFIDENCE_VALUES = ['high', 'medium', 'low', 'unverified'] as const;
export type Confidence = (typeof CONFIDENCE_VALUES)[number];

export const REVIEW_STATE_VALUES = ['reported', 'unreported', 'not-applicable', 'not-reviewed'] as const;
export type ReviewState = (typeof REVIEW_STATE_VALUES)[number];

export const PRIMITIVE_ROLE_VALUES = ['workflow', 'mechanism', 'validation'] as const;
export type PrimitiveRole = (typeof PRIMITIVE_ROLE_VALUES)[number];

export const OBSERVATION_CATEGORY_VALUES = ['effectiveness', 'adoption-output', 'cost-latency', 'implementation-scale', 'runtime-capacity'] as const;
export type ObservationCategory = (typeof OBSERVATION_CATEGORY_VALUES)[number];

export const OBSERVATION_BASIS_VALUES = ['reported-measurement', 'qualitative', 'estimate', 'target'] as const;
export type ObservationBasis = (typeof OBSERVATION_BASIS_VALUES)[number];
