export type NodeType =
  | 'Material'
  | 'Process'
  | 'Equipment'
  | 'Property'
  | 'Experiment'
  | 'Publication'
  | 'Expert'
  | 'Facility'

export type EdgeFlag = 'normal' | 'contradiction' | 'gap'

export type Confidence = 'high' | 'medium' | 'low'

import type { SearchFilters } from './filters'

export interface AskRequest {
  question: string
  filters?: SearchFilters
}

export interface AnswerLink {
  nodeId: string
  start: number
  end: number
  label?: string
}

export interface Source {
  doc_id: string
  title: string
  year: number
  snippet: string
}

export interface GraphNode {
  id: string
  label: string
  type: NodeType
  geo?: string
}

export interface GraphEdge {
  from: string
  to: string
  label: string
  flag: EdgeFlag
}

export interface GraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

export interface Contradiction {
  about: string
  sources: string[]
}

export interface Gap {
  material: string
  process: string
  reason: string
  score: number
}

export interface AskResponse {
  answer: string
  answer_links?: AnswerLink[]
  sources: Source[]
  confidence: Confidence
  graph: GraphData
  gaps: Gap[]
  contradictions: Contradiction[]
}
