import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { API_BASE_URL, USE_MOCK } from '@/shared/config/env'
import { MOCK_DOCUMENTS } from '@/shared/mocks/documents'
import type { AskResponse } from '@/shared/types/ask'
import type { Document } from '@/shared/types/document'
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
    getDocument: builder.query<Document, string>({
      queryFn: async (docId, _api, _extraOptions, baseQuery) => {
        if (USE_MOCK) {
          const doc = MOCK_DOCUMENTS[docId]
          if (!doc) {
            return { error: { status: 404, data: 'Документ не найден' } }
          }
          return { data: doc }
        }

        const result = await baseQuery({ url: `/document/${encodeURIComponent(docId)}` })
        if (result.error) {
          return { error: result.error }
        }
        return { data: result.data as Document }
      },
    }),
  }),
})

export const { useAskQuestionMutation, useGetDocumentQuery } = baseApi
