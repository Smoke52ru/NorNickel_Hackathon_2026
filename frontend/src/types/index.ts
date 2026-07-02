// Core entity types for the knowledge graph system

export interface Entity {
  id: string
  type: EntityType
  name: string
  description?: string
  properties: Record<string, unknown>
  createdAt: string
  updatedAt: string
}

export enum EntityType {
  ARTICLE = 'article',
  EXPERIMENT = 'experiment',
  MATERIAL = 'material',
  PROPERTY = 'property',
  MODE = 'mode',
  EQUIPMENT = 'equipment',
  TEAM = 'team',
  PERSON = 'person',
}

export interface Relationship {
  id: string
  sourceId: string
  targetId: string
  type: RelationshipType
  properties?: Record<string, unknown>
}

export enum RelationshipType {
  MENTIONED_IN = 'mentioned_in',
  TESTED_IN = 'tested_in',
  HAS_PROPERTY = 'has_property',
  USED_MODE = 'used_mode',
  USED_EQUIPMENT = 'used_equipment',
  CONDUCTED_BY = 'conducted_by',
  MEMBER_OF = 'member_of',
  RELATED_TO = 'related_to',
}

export interface SearchResult {
  entities: Entity[]
  relationships: Relationship[]
  total: number
}

export interface GraphData {
  nodes: Entity[]
  edges: Relationship[]
}

export interface FilterOptions {
  entityTypes?: EntityType[]
  dateRange?: { from: string; to: string }
  properties?: Record<string, unknown>
}