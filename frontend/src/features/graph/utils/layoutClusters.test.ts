import { describe, expect, it } from 'vitest'
import { detectClusters } from './detectClusters'
import { layoutClusters } from './layoutClusters'

describe('layoutClusters', () => {
  it('places nodes from different clusters far apart', () => {
    const graph = {
      nodes: [
        { id: 'a1', label: 'A1', type: 'Material' as const },
        { id: 'a2', label: 'Process A', type: 'Process' as const },
        { id: 'b1', label: 'B1', type: 'Material' as const },
        { id: 'b2', label: 'Process B', type: 'Process' as const },
      ],
      edges: [
        { from: 'a1', to: 'a2', label: 'uses_material', flag: 'normal' as const },
        { from: 'b1', to: 'b2', label: 'uses_material', flag: 'normal' as const },
      ],
    }

    const clusterResult = detectClusters(graph)
    const positions = layoutClusters(graph, clusterResult)
    const posA1 = positions.get('a1')!
    const posB1 = positions.get('b1')!

    expect(Math.hypot(posA1.x - posB1.x, posA1.y - posB1.y)).toBeGreaterThan(300)
  })

  it('places nodes within a cluster closer together', () => {
    const graph = {
      nodes: [
        { id: 'a1', label: 'A1', type: 'Material' as const },
        { id: 'a2', label: 'Process A', type: 'Process' as const },
        { id: 'a3', label: 'A3', type: 'Equipment' as const },
        { id: 'a4', label: 'A4', type: 'Property' as const },
      ],
      edges: [
        { from: 'a1', to: 'a2', label: 'uses_material', flag: 'normal' as const },
        { from: 'a2', to: 'a3', label: 'part_of', flag: 'normal' as const },
        { from: 'a3', to: 'a4', label: 'operates_at_condition', flag: 'normal' as const },
        { from: 'a4', to: 'a1', label: 'produces_output', flag: 'normal' as const },
        { from: 'a1', to: 'a3', label: 'uses_material', flag: 'normal' as const },
      ],
    }

    const clusterResult = {
      clusters: [{ id: 0, name: 'Process A', nodeIds: ['a1', 'a2', 'a3', 'a4'] }],
      nodeCluster: new Map([
        ['a1', 0],
        ['a2', 0],
        ['a3', 0],
        ['a4', 0],
      ]),
      bridgeEdges: new Set<string>(),
    }
    const positions = layoutClusters(graph, clusterResult)
    const posA1 = positions.get('a1')!
    const posA2 = positions.get('a2')!

    expect(Math.hypot(posA1.x - posA2.x, posA1.y - posA2.y)).toBeLessThan(200)
  })
})
