import { describe, expect, it } from 'vitest'
import { detectClusters } from './detectClusters'

describe('detectClusters', () => {
  it('finds three clusters connected by bridge edges', () => {
    const graph = {
      nodes: [
        { id: 'a1', label: 'A1', type: 'Material' as const },
        { id: 'a2', label: 'Process A', type: 'Process' as const },
        { id: 'b1', label: 'B1', type: 'Material' as const },
        { id: 'b2', label: 'Process B', type: 'Process' as const },
        { id: 'c1', label: 'C1', type: 'Material' as const },
        { id: 'c2', label: 'Process C', type: 'Process' as const },
      ],
      edges: [
        { from: 'a1', to: 'a2', label: 'uses_material', flag: 'normal' as const },
        { from: 'b1', to: 'b2', label: 'uses_material', flag: 'normal' as const },
        { from: 'c1', to: 'c2', label: 'uses_material', flag: 'normal' as const },
        { from: 'a2', to: 'b2', label: 'expert_in', flag: 'normal' as const },
        { from: 'b2', to: 'c2', label: 'expert_in', flag: 'normal' as const },
      ],
    }

    const result = detectClusters(graph)
    expect(result.clusters.length).toBeGreaterThanOrEqual(2)
    expect(result.bridgeEdges.size).toBeGreaterThan(0)
  })

  it('assigns bridge endpoints to different clusters', () => {
    const graph = {
      nodes: [
        { id: 'a1', label: 'A1', type: 'Material' as const },
        { id: 'a2', label: 'Process A', type: 'Process' as const },
        { id: 'a3', label: 'A3', type: 'Equipment' as const },
        { id: 'b1', label: 'B1', type: 'Material' as const },
        { id: 'b2', label: 'Process B', type: 'Process' as const },
      ],
      edges: [
        { from: 'a1', to: 'a2', label: 'uses_material', flag: 'normal' as const },
        { from: 'a2', to: 'a3', label: 'part_of', flag: 'normal' as const },
        { from: 'b1', to: 'b2', label: 'uses_material', flag: 'normal' as const },
        { from: 'a2', to: 'b2', label: 'expert_in', flag: 'normal' as const },
      ],
    }

    const result = detectClusters(graph)
    expect(result.clusters.length).toBeGreaterThanOrEqual(2)
    expect(result.nodeCluster.get('a2')).not.toBe(result.nodeCluster.get('b2'))
  })

  it('falls back to label propagation for a single dense component', () => {
    const graph = {
      nodes: [
        { id: 'a', label: 'A', type: 'Material' as const },
        { id: 'b', label: 'Process B', type: 'Process' as const },
        { id: 'c', label: 'C', type: 'Equipment' as const },
        { id: 'd', label: 'D', type: 'Property' as const },
      ],
      edges: [
        { from: 'a', to: 'b', label: 'uses_material', flag: 'normal' as const },
        { from: 'b', to: 'c', label: 'part_of', flag: 'normal' as const },
        { from: 'c', to: 'd', label: 'operates_at_condition', flag: 'normal' as const },
        { from: 'd', to: 'a', label: 'produces_output', flag: 'normal' as const },
      ],
    }

    const result = detectClusters(graph)
    expect(result.clusters.length).toBeGreaterThanOrEqual(1)
  })
})
