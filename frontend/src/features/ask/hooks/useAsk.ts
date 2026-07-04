import { useCallback, useState } from 'react'
import { useAskQuestionMutation } from '@/shared/api/baseApi'
import { USE_MOCK } from '@/shared/config/env'
import type { AskResponse } from '@/shared/types/ask'
import { useAppSelector } from '@/app/hooks'
import mockResponse from '@/shared/mocks/askResponse.json'

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export function useAsk() {
  const [askQuestion, { isLoading, isError, error }] = useAskQuestionMutation()
  const [data, setData] = useState<AskResponse | null>(null)
  const filters = useAppSelector((state) => state.settings.filters)

  const ask = useCallback(
    async (question: string) => {
      const requestBody = {
        question,
        filters,
      }

      if (USE_MOCK) {
        await delay(500)
        setData({
          ...mockResponse,
          answer: mockResponse.answer.replace(
            'Для обессоливания',
            `По запросу «${question}»: для обессоливания`,
          ),
        } as AskResponse)
        return
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
