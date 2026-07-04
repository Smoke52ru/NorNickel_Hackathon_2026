import { useCallback, useState } from 'react'
import { useAskQuestionMutation } from '@/shared/api/baseApi'
import type { AskResponse } from '@/shared/types/ask'
import type { SearchFilters } from '@/shared/types/filters'
import { useAppSelector } from '@/app/hooks'
import { mapFiltersToApi } from '@/shared/utils/mapFiltersToApi'

export function useAsk() {
  const [askQuestion, { isLoading, isError, error }] = useAskQuestionMutation()
  const [data, setData] = useState<AskResponse | null>(null)
  const filters = useAppSelector((state) => state.settings.filters)

  const ask = useCallback(
    async (question: string, filtersOverride?: SearchFilters) => {
      const activeFilters = filtersOverride ?? filters
      const requestBody = {
        question,
        filters: mapFiltersToApi(activeFilters),
      }
      try {
        const result = await askQuestion(requestBody).unwrap()
        setData(result)
      } catch {
        setData(null)
      }
    },
    [askQuestion, filters],
  )

  const reset = useCallback(() => {
    setData(null)
  }, [])

  return {
    ask,
    reset,
    data,
    isLoading,
    isError,
    error,
  }
}
