import type { SearchFilters } from '@/shared/types/filters'
import { isAllNodeTypesSelected } from '@/shared/types/filters'

export interface ApiFilters {
  geo?: 'ru' | 'foreign'
  year_from?: number
  year_to?: number
  types?: string[]
}

export function mapFiltersToApi(filters: SearchFilters): ApiFilters | undefined {
  const api: ApiFilters = {}

  if (filters.geography === 'domestic') {
    api.geo = 'ru'
  } else if (filters.geography === 'foreign') {
    api.geo = 'foreign'
  }

  if (filters.yearFrom !== null) {
    api.year_from = filters.yearFrom
  }

  if (filters.yearTo !== null) {
    api.year_to = filters.yearTo
  }

  if (
    filters.nodeTypes.length > 0 &&
    !isAllNodeTypesSelected(filters.nodeTypes)
  ) {
    api.types = filters.nodeTypes
  }

  return Object.keys(api).length > 0 ? api : undefined
}
