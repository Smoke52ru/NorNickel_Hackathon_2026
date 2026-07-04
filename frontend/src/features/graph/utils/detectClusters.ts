import type { EdgeFlag, GraphData, GraphEdge, NodeType } from '@/shared/types/ask'

export interface ClusterInfo {
  id: number
  name: string
  nodeIds: string[]
}

export interface ClusterResult {
  clusters: ClusterInfo[]
  nodeCluster: Map<string, number>
  bridgeEdges: Set<string>
}

const TYPE_PRIORITY: Record<NodeType, number> = {
  Process: 3,
  Material: 2,
  Equipment: 1,
  Property: 1,
  Experiment: 1,
  Publication: 1,
  Expert: 1,
  Facility: 1,
}

const FLAG_WEIGHT: Record<EdgeFlag, number> = {
  normal: 1.0,
  contradiction: 0.5,
  gap: 0.25,
}

function edgeKey(from: string, to: string): string {
  return `${from}|${to}`
}

function buildAdjacency(graph: GraphData): Map<string, string[]> {
  const adjacency = new Map<string, string[]>()
  for (const node of graph.nodes) {
    adjacency.set(node.id, [])
  }
  for (const edge of graph.edges) {
    adjacency.get(edge.from)?.push(edge.to)
    adjacency.get(edge.to)?.push(edge.from)
  }
  return adjacency
}

function edgeBetweenness(graph: GraphData): Map<string, number> {
  const adjacency = buildAdjacency(graph)
  const scores = new Map<string, number>()

  for (const edge of graph.edges) {
    scores.set(edgeKey(edge.from, edge.to), 0)
    scores.set(edgeKey(edge.to, edge.from), 0)
  }

  for (const source of graph.nodes.map((node) => node.id)) {
    const stack: string[] = []
    const pred = new Map<string, string[]>()
    const sigma = new Map<string, number>()
    const dist = new Map<string, number>()

    for (const node of graph.nodes) {
      pred.set(node.id, [])
      sigma.set(node.id, 0)
      dist.set(node.id, -1)
    }

    sigma.set(source, 1)
    dist.set(source, 0)
    const queue = [source]

    while (queue.length > 0) {
      const v = queue.shift()!
      stack.push(v)
      for (const w of adjacency.get(v) ?? []) {
        if (dist.get(w)! === -1) {
          dist.set(w, dist.get(v)! + 1)
          queue.push(w)
        }
        if (dist.get(w) === dist.get(v)! + 1) {
          sigma.set(w, sigma.get(w)! + sigma.get(v)!)
          pred.get(w)!.push(v)
        }
      }
    }

    const delta = new Map<string, number>()
    for (const node of graph.nodes) delta.set(node.id, 0)

    while (stack.length > 0) {
      const w = stack.pop()!
      for (const v of pred.get(w) ?? []) {
        const contribution = (sigma.get(v)! / sigma.get(w!)!) * (1 + delta.get(w!)!)
        delta.set(v, delta.get(v)! + contribution)
        const key = edgeKey(v, w)
        scores.set(key, (scores.get(key) ?? 0) + contribution)
      }
      if (w !== source) delta.set(w, delta.get(w)! + 1)
    }
  }

  return scores
}

function findConnectedComponents(
  graph: GraphData,
  excludedEdges: Set<string>,
): string[][] {
  const adjacency = new Map<string, Set<string>>()
  for (const node of graph.nodes) adjacency.set(node.id, new Set())
  for (const edge of graph.edges) {
    if (excludedEdges.has(edgeKey(edge.from, edge.to))) continue
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
        if (!visited.has(neighbor)) stack.push(neighbor)
      }
    }
    components.push(component)
  }

  return components
}

function splitByBetweenness(graph: GraphData): string[][] {
  if (graph.nodes.length <= 2) {
    return [graph.nodes.map((node) => node.id)]
  }

  const betweenness = edgeBetweenness(graph)
  const rankedEdges = [...graph.edges].sort(
    (a, b) =>
      (betweenness.get(edgeKey(b.from, b.to)) ?? 0) -
      (betweenness.get(edgeKey(a.from, a.to)) ?? 0),
  )

  const excluded = new Set<string>()
  let components = findConnectedComponents(graph, excluded)

  const targetParts = Math.min(
    3,
    Math.max(2, Math.round(graph.nodes.length / 9)),
  )

  for (const edge of rankedEdges) {
    if (components.length >= targetParts) break
    excluded.add(edgeKey(edge.from, edge.to))
    excluded.add(edgeKey(edge.to, edge.from))
    const next = findConnectedComponents(graph, excluded)
    if (next.length > components.length) {
      components = next
    }
  }

  return components.filter((component) => component.length > 0)
}

function weightedLabelPropagation(
  graph: GraphData,
  seed: Map<string, number>,
  iterations = 15,
): Map<string, number> {
  const labels = new Map(seed)
  const neighbors = new Map<string, Array<{ id: string; weight: number }>>()
  for (const node of graph.nodes) neighbors.set(node.id, [])
  for (const edge of graph.edges) {
    const weight = FLAG_WEIGHT[edge.flag]
    neighbors.get(edge.from)?.push({ id: edge.to, weight })
    neighbors.get(edge.to)?.push({ id: edge.from, weight })
  }

  for (let i = 0; i < iterations; i += 1) {
    const next = new Map(labels)
    for (const node of graph.nodes) {
      const scores = new Map<number, number>()
      for (const { id, weight } of neighbors.get(node.id) ?? []) {
        const label = labels.get(id)!
        scores.set(label, (scores.get(label) ?? 0) + weight)
      }
      if (scores.size === 0) continue
      let bestLabel = labels.get(node.id)!
      let bestScore = -1
      for (const [label, score] of scores) {
        if (score > bestScore) {
          bestScore = score
          bestLabel = label
        }
      }
      next.set(node.id, bestLabel)
    }
    for (const [id, label] of next) labels.set(id, label)
  }

  return labels
}

function normalizeClusterIds(raw: Map<string, number>): Map<string, number> {
  const remap = new Map<number, number>()
  const normalized = new Map<string, number>()
  let nextId = 0
  for (const node of raw.keys()) {
    const old = raw.get(node)!
    if (!remap.has(old)) {
      remap.set(old, nextId)
      nextId += 1
    }
    normalized.set(node, remap.get(old)!)
  }
  return normalized
}

function nameCluster(clusterNodeIds: string[], graph: GraphData): string {
  const nodes = graph.nodes.filter((node) => clusterNodeIds.includes(node.id))
  const weightedDegree = (nodeId: string) =>
    graph.edges.filter((edge) => edge.from === nodeId || edge.to === nodeId).length

  nodes.sort((a, b) => {
    const typeDiff = TYPE_PRIORITY[b.type] - TYPE_PRIORITY[a.type]
    if (typeDiff !== 0) return typeDiff
    return weightedDegree(b.id) - weightedDegree(a.id)
  })

  return nodes[0]?.label ?? 'Кластер'
}

function buildClusterResult(
  graph: GraphData,
  nodeCluster: Map<string, number>,
): ClusterResult {
  const bridgeEdges = new Set<string>()
  for (const edge of graph.edges) {
    if (nodeCluster.get(edge.from) !== nodeCluster.get(edge.to)) {
      bridgeEdges.add(edgeKey(edge.from, edge.to))
      bridgeEdges.add(edgeKey(edge.to, edge.from))
    }
  }

  const byId = new Map<number, string[]>()
  for (const [nodeId, clusterId] of nodeCluster) {
    const list = byId.get(clusterId) ?? []
    list.push(nodeId)
    byId.set(clusterId, list)
  }

  const clusters: ClusterInfo[] = [...byId.entries()]
    .sort(([a], [b]) => a - b)
    .map(([id, nodeIds]) => ({
      id,
      name: nameCluster(nodeIds, graph),
      nodeIds,
    }))

  return { clusters, nodeCluster, bridgeEdges }
}

export function detectClusters(graph: GraphData): ClusterResult {
  if (graph.nodes.length === 0) {
    return { clusters: [], nodeCluster: new Map(), bridgeEdges: new Set() }
  }

  const components = splitByBetweenness(graph)

  if (components.length >= 2) {
    const nodeCluster = new Map<string, number>()
    components.forEach((component, index) => {
      for (const nodeId of component) nodeCluster.set(nodeId, index)
    })
    return buildClusterResult(graph, normalizeClusterIds(nodeCluster))
  }

  const seed = new Map<string, number>()
  graph.nodes.forEach((node, index) => seed.set(node.id, index))
  const nodeCluster = normalizeClusterIds(weightedLabelPropagation(graph, seed))
  return buildClusterResult(graph, nodeCluster)
}

export function isBridgeEdge(edge: GraphEdge, bridgeEdges: Set<string>): boolean {
  return bridgeEdges.has(edgeKey(edge.from, edge.to))
}
