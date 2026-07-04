import { describe, expect, it } from 'vitest'
import { layoutComponents } from './layoutComponents'

describe('layoutComponents', () => {
  it('places disconnected components far apart', () => {
    const graph = {
      nodes: [
        { id: 'a', label: 'A', type: 'Material' as const },
        { id: 'b', label: 'B', type: 'Process' as const },
        { id: 'c', label: 'C', type: 'Material' as const },
      ],
      edges: [{ from: 'a', to: 'b', label: 'uses_material', flag: 'normal' as const }],
    }

    const positions = layoutComponents(graph)
    const posA = positions.get('a')!
    const posC = positions.get('c')!

    const distance = Math.hypot(posA.x - posC.x, posA.y - posC.y)
    expect(distance).toBeGreaterThan(200)
  })

  it('places connected nodes closer together', () => {
    const graph = {
      nodes: [
        { id: 'a', label: 'A', type: 'Material' as const },
        { id: 'b', label: 'B', type: 'Process' as const },
      ],
      edges: [{ from: 'a', to: 'b', label: 'uses_material', flag: 'normal' as const }],
    }

    const positions = layoutComponents(graph)
    const posA = positions.get('a')!
    const posB = positions.get('b')!

    const distance = Math.hypot(posA.x - posB.x, posA.y - posB.y)
    expect(distance).toBeLessThan(200)
  })
})
