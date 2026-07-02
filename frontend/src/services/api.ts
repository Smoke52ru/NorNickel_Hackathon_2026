import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth tokens if needed
api.interceptors.request.use(
  (config) => {
    // Add auth token logic here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Example API functions for the knowledge graph system
export const searchApi = {
  search: (query: string) => api.get(`/search?q=${encodeURIComponent(query)}`),
  getEntity: (id: string) => api.get(`/entities/${id}`),
  getRelated: (id: string) => api.get(`/entities/${id}/related`),
}

export const graphApi = {
  getGraph: (filters?: Record<string, unknown>) => api.post('/graph', filters),
  getNodes: () => api.get('/graph/nodes'),
  getEdges: () => api.get('/graph/edges'),
}