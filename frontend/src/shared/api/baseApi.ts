import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { API_BASE_URL } from '@/shared/config/env'
import type { AskResponse } from '@/shared/types/ask'
import type { ApiFilters } from '@/shared/utils/mapFiltersToApi'

export interface AskRequestBody {
  question: string
  filters?: ApiFilters
}

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
  }),
  endpoints: (builder) => ({
    askQuestion: builder.mutation<AskResponse, AskRequestBody>({
      query: (body) => ({
        url: '/ask',
        method: 'POST',
        body,
      }),
    }),
  }),
})

export const { useAskQuestionMutation } = baseApi
