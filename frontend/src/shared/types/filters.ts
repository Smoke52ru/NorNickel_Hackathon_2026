import { NODE_TYPE_LABELS } from '@/features/graph/config/nodeStyles'
import type { NodeType } from '@/shared/types/ask'

export type GeographyFilter = 'all' | 'domestic' | 'foreign'
export type ConfidenceFilter = 'high' | 'medium' | 'low'

export const ALL_NODE_TYPES = Object.keys(NODE_TYPE_LABELS) as NodeType[]

export interface SearchFilters {
  nodeTypes: NodeType[]
  geography: GeographyFilter
  yearFrom: number | null
  yearTo: number | null
  minConfidence: ConfidenceFilter
  materialKeyword: string
  processKeyword: string
  showContradictions: boolean
  showGaps: boolean
}

export const DEFAULT_FILTERS: SearchFilters = {
  nodeTypes: [...ALL_NODE_TYPES],
  geography: 'all',
  yearFrom: null,
  yearTo: null,
  minConfidence: 'low',
  materialKeyword: '',
  processKeyword: '',
  showContradictions: true,
  showGaps: true,
}

export function isAllNodeTypesSelected(nodeTypes: NodeType[]): boolean {
  if (nodeTypes.length !== ALL_NODE_TYPES.length) return false
  return ALL_NODE_TYPES.every((type) => nodeTypes.includes(type))
}

const CONFIDENCE_ORDER: Record<ConfidenceFilter, number> = {
  low: 0,
  medium: 1,
  high: 2,
}

export function meetsMinConfidence(
  actual: ConfidenceFilter,
  minimum: ConfidenceFilter,
): boolean {
  return CONFIDENCE_ORDER[actual] >= CONFIDENCE_ORDER[minimum]
}
