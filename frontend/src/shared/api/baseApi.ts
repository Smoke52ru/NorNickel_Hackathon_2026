import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { AskRequest, AskResponse } from '@/shared/types/ask'

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL || '/api',
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
