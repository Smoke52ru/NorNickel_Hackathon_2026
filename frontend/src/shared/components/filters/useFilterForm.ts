import { useEffect, useState } from 'react'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import { resetFilters, setFilters } from '@/app/settingsSlice'
import {
  DEFAULT_FILTERS,
  type SearchFilters,
} from '@/shared/types/filters'
import { YEAR_MAX, YEAR_MIN } from './FilterControls'

interface UseFilterFormOptions {
  syncWhenOpen?: boolean
  open?: boolean
  onApplied?: (next: SearchFilters, prev: SearchFilters) => void
}

export function useFilterForm(options: UseFilterFormOptions = {}) {
  const { syncWhenOpen = false, open = true, onApplied } = options
  const dispatch = useAppDispatch()
  const savedFilters = useAppSelector((state) => state.settings.filters)
  const [draft, setDraft] = useState<SearchFilters>(savedFilters)
  const [yearRange, setYearRange] = useState<[number, number]>([
    savedFilters.yearFrom ?? YEAR_MIN,
    savedFilters.yearTo ?? YEAR_MAX,
  ])

  useEffect(() => {
    if (!syncWhenOpen || open) {
      setDraft(savedFilters)
      setYearRange([
        savedFilters.yearFrom ?? YEAR_MIN,
        savedFilters.yearTo ?? YEAR_MAX,
      ])
    }
  }, [syncWhenOpen, open, savedFilters])

  const buildNext = (): SearchFilters => ({
    ...draft,
    yearFrom: yearRange[0] === YEAR_MIN ? null : yearRange[0],
    yearTo: yearRange[1] === YEAR_MAX ? null : yearRange[1],
  })

  const apply = () => {
    const prev = savedFilters
    const next = buildNext()
    dispatch(setFilters(next))
    onApplied?.(next, prev)
  }

  const reset = () => {
    setDraft(DEFAULT_FILTERS)
    setYearRange([YEAR_MIN, YEAR_MAX])
    dispatch(resetFilters())
    onApplied?.(DEFAULT_FILTERS, savedFilters)
  }

  return {
    draft,
    setDraft,
    yearRange,
    setYearRange,
    apply,
    reset,
  }
}
