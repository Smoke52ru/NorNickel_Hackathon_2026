import type { SearchFilters } from '@/shared/types/filters'
import { mapFiltersToApi } from './mapFiltersToApi'

function serverFilterSignature(filters: SearchFilters): string {
  return JSON.stringify(mapFiltersToApi(filters) ?? {})
}

/** True when backend /ask must be called again for the new filter values. */
export function filtersNeedServerRefetch(
  prev: SearchFilters,
  next: SearchFilters,
): boolean {
  return serverFilterSignature(prev) !== serverFilterSignature(next)
}
