import type { GraphData } from '@/shared/types/ask'

export interface NodePosition {
  x: number
  y: number
}

const COMPONENT_SPACING = 450
const INNER_RADIUS = 80

function findConnectedComponents(graph: GraphData): string[][] {
  const adjacency = new Map<string, Set<string>>()

  for (const node of graph.nodes) {
    adjacency.set(node.id, new Set())
  }

  for (const edge of graph.edges) {
    adjacency.get(edge.from)?.add(edge.to)
    adjacency.get(edge.to)?.add(edge.from)
  }

  const visited = new Set<string>()
  const components: string[][] = []

  for (const node of graph.nodes) {
    if (visited.has(node.id)) continue

    const stack = [node.id]
    const component: string[] = []

    while (stack.length > 0) {
      const current = stack.pop()!
      if (visited.has(current)) continue
      visited.add(current)
      component.push(current)

      for (const neighbor of adjacency.get(current) ?? []) {
        if (!visited.has(neighbor)) {
          stack.push(neighbor)
        }
      }
    }

    components.push(component)
  }

  return components
}

export function layoutComponents(graph: GraphData): Map<string, NodePosition> {
  const positions = new Map<string, NodePosition>()
  const components = findConnectedComponents(graph)

  const cols = Math.ceil(Math.sqrt(components.length))

  components.forEach((component, index) => {
    const col = index % cols
    const row = Math.floor(index / cols)
    const centerX = col * COMPONENT_SPACING
    const centerY = row * COMPONENT_SPACING

    if (component.length === 1) {
      positions.set(component[0], { x: centerX, y: centerY })
      return
    }

    component.forEach((nodeId, nodeIndex) => {
      const angle = (2 * Math.PI * nodeIndex) / component.length
      positions.set(nodeId, {
        x: centerX + INNER_RADIUS * Math.cos(angle),
        y: centerY + INNER_RADIUS * Math.sin(angle),
      })
    })
  })

  return positions
}
