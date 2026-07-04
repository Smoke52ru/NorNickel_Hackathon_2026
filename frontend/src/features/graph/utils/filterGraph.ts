import type { GraphData, GraphNode } from '@/shared/types/ask'
import { isAllNodeTypesSelected, type SearchFilters } from '@/shared/types/filters'

function matchesKeyword(label: string, keyword: string): boolean {
  if (!keyword.trim()) return true
  return label.toLowerCase().includes(keyword.trim().toLowerCase())
}

function matchesGeography(
  node: GraphNode & { geo?: string },
  geography: SearchFilters['geography'],
): boolean {
  if (geography === 'all') return true
  if (!node.geo) return true
  if (geography === 'domestic') return node.geo === 'ru'
  if (geography === 'foreign') return node.geo === 'foreign'
  return true
}

export function filterGraph(
  graph: GraphData | null,
  filters: SearchFilters,
): GraphData | null {
  if (!graph) return null

  let nodes = graph.nodes.filter((node) => {
    if (!matchesGeography(node, filters.geography)) return false
    if (
      filters.materialKeyword &&
      node.type === 'Material' &&
      !matchesKeyword(node.label, filters.materialKeyword)
    ) {
      return false
    }
    if (
      filters.processKeyword &&
      node.type === 'Process' &&
      !matchesKeyword(node.label, filters.processKeyword)
    ) {
      return false
    }
    return true
  })

  if (
    filters.nodeTypes.length > 0 &&
    !isAllNodeTypesSelected(filters.nodeTypes)
  ) {
    nodes = nodes.filter((node) => filters.nodeTypes.includes(node.type))
  }

  const nodeIds = new Set(nodes.map((node) => node.id))

  let edges = graph.edges.filter(
    (edge) => nodeIds.has(edge.from) && nodeIds.has(edge.to),
  )

  if (!filters.showContradictions) {
    edges = edges.filter((edge) => edge.flag !== 'contradiction')
  }

  if (!filters.showGaps) {
    edges = edges.filter((edge) => edge.flag !== 'gap')
  }

  return { nodes, edges }
}
