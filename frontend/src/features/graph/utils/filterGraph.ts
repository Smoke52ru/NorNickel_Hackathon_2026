import type { GraphData } from '@/shared/types/ask'
import type { SearchFilters } from '@/shared/types/filters'

export function filterGraph(
  graph: GraphData | null,
  filters: SearchFilters,
): GraphData | null {
  if (!graph) return null

  let nodes = graph.nodes

  if (filters.nodeTypes.length > 0) {
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
