import type { NodeType } from './ask'

export type GeographyFilter = 'all' | 'domestic' | 'foreign'
export type ConfidenceFilter = 'high' | 'medium' | 'low'

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
  nodeTypes: [],
  geography: 'all',
  yearFrom: null,
  yearTo: null,
  minConfidence: 'low',
  materialKeyword: '',
  processKeyword: '',
  showContradictions: true,
  showGaps: true,
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
