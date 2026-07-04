import { describe, expect, it } from 'vitest'
import { DEFAULT_FILTERS } from '@/shared/types/filters'
import { mapFiltersToApi } from './mapFiltersToApi'

describe('mapFiltersToApi', () => {
  it('returns undefined for default filters', () => {
    expect(mapFiltersToApi(DEFAULT_FILTERS)).toBeUndefined()
  })

  it('maps domestic geography to geo ru', () => {
    expect(
      mapFiltersToApi({ ...DEFAULT_FILTERS, geography: 'domestic' }),
    ).toEqual({ geo: 'ru' })
  })

  it('maps foreign geography to geo foreign', () => {
    expect(
      mapFiltersToApi({ ...DEFAULT_FILTERS, geography: 'foreign' }),
    ).toEqual({ geo: 'foreign' })
  })

  it('maps nodeTypes to types when subset selected', () => {
    expect(
      mapFiltersToApi({ ...DEFAULT_FILTERS, nodeTypes: ['Material'] }),
    ).toEqual({ types: ['Material'] })
  })

  it('omits types when all node types are selected', () => {
    expect(mapFiltersToApi(DEFAULT_FILTERS)).toBeUndefined()
  })

  it('maps year range to snake_case', () => {
    expect(
      mapFiltersToApi({
        ...DEFAULT_FILTERS,
        yearFrom: 2020,
        yearTo: 2024,
      }),
    ).toEqual({ year_from: 2020, year_to: 2024 })
  })

  it('combines multiple filters', () => {
    expect(
      mapFiltersToApi({
        ...DEFAULT_FILTERS,
        geography: 'domestic',
        nodeTypes: ['Material', 'Process'],
        yearFrom: 2018,
      }),
    ).toEqual({
      geo: 'ru',
      types: ['Material', 'Process'],
      year_from: 2018,
    })
  })
})
