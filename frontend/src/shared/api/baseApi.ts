import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type {
  Entity,
  FilterOptions,
  GraphData,
  Relationship,
  SearchResult,
} from '@/shared/types'

export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl: import.meta.env.VITE_API_URL || '/api',
  }),
  tagTypes: ['Entity', 'Graph'],
  endpoints: (builder) => ({
    searchEntities: builder.query<SearchResult, string>({
      query: (q) => `/search?q=${encodeURIComponent(q)}`,
      providesTags: ['Entity'],
    }),
    getEntity: builder.query<Entity, string>({
      query: (id) => `/entities/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'Entity', id }],
    }),
    getRelatedEntities: builder.query<Entity[], string>({
      query: (id) => `/entities/${id}/related`,
      providesTags: ['Entity'],
    }),
    getGraph: builder.query<GraphData, FilterOptions | void>({
      query: (filters) => ({
        url: '/graph',
        method: 'POST',
        body: filters,
      }),
      providesTags: ['Graph'],
    }),
    getGraphNodes: builder.query<Entity[], void>({
      query: () => '/graph/nodes',
      providesTags: ['Graph'],
    }),
    getGraphEdges: builder.query<Relationship[], void>({
      query: () => '/graph/edges',
      providesTags: ['Graph'],
    }),
  }),
})

export const {
  useSearchEntitiesQuery,
  useGetEntityQuery,
  useGetRelatedEntitiesQuery,
  useGetGraphQuery,
  useGetGraphNodesQuery,
  useGetGraphEdgesQuery,
} = baseApi
