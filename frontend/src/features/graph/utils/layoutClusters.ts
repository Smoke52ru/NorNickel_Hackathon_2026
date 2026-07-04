import type { GraphData } from '@/shared/types/ask'
import type { ClusterResult } from './detectClusters'

export interface NodePosition {
  x: number
  y: number
}

const CLUSTER_SPACING = 500
const INNER_RADIUS = 80

export function layoutClusters(
  _graph: GraphData,
  clusterResult: ClusterResult,
): Map<string, NodePosition> {
  const positions = new Map<string, NodePosition>()
  const { clusters } = clusterResult

  if (clusters.length === 0) return positions

  const cols = Math.ceil(Math.sqrt(clusters.length))

  clusters.forEach((cluster, index) => {
    const col = index % cols
    const row = Math.floor(index / cols)
    const centerX = col * CLUSTER_SPACING
    const centerY = row * CLUSTER_SPACING
    const radius = INNER_RADIUS + 8 * Math.sqrt(cluster.nodeIds.length)

    if (cluster.nodeIds.length === 1) {
      positions.set(cluster.nodeIds[0], { x: centerX, y: centerY })
      return
    }

    cluster.nodeIds.forEach((nodeId, nodeIndex) => {
      const angle = (2 * Math.PI * nodeIndex) / cluster.nodeIds.length
      positions.set(nodeId, {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle),
      })
    })
  })

  return positions
}
