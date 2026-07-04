import { describe, expect, it } from 'vitest'
import { DEFAULT_FILTERS } from '@/shared/types/filters'
import { filtersNeedServerRefetch } from './filterRefetch'

describe('filtersNeedServerRefetch', () => {
  it('returns false for client-only filter changes', () => {
    expect(
      filtersNeedServerRefetch(DEFAULT_FILTERS, {
        ...DEFAULT_FILTERS,
        minConfidence: 'high',
        materialKeyword: 'никель',
        showContradictions: false,
      }),
    ).toBe(false)
  })

  it('returns true when geography changes', () => {
    expect(
      filtersNeedServerRefetch(DEFAULT_FILTERS, {
        ...DEFAULT_FILTERS,
        geography: 'domestic',
      }),
    ).toBe(true)
  })

  it('returns true when year range changes', () => {
    expect(
      filtersNeedServerRefetch(DEFAULT_FILTERS, {
        ...DEFAULT_FILTERS,
        yearFrom: 2020,
      }),
    ).toBe(true)
  })

  it('returns true when node type subset changes', () => {
    expect(
      filtersNeedServerRefetch(DEFAULT_FILTERS, {
        ...DEFAULT_FILTERS,
        nodeTypes: ['Material'],
      }),
    ).toBe(true)
  })
})
