import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { API_BASE_URL } from '@/shared/config/env'
import type { AskRequest, AskResponse } from '@/shared/types/ask'

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
  }),
  endpoints: (builder) => ({
    askQuestion: builder.mutation<AskResponse, AskRequest>({
      query: (body) => ({
        url: '/ask',
        method: 'POST',
        body,
      }),
    }),
  }),
})

export const { useAskQuestionMutation } = baseApi
