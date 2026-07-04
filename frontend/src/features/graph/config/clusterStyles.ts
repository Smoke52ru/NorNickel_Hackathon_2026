export const CLUSTER_BORDER_COLORS = [
  '#597ef7',
  '#73d13d',
  '#9254de',
  '#ffa940',
  '#36cfc9',
  '#ff85c0',
]

export function getClusterBorderColor(clusterId: number): string {
  return CLUSTER_BORDER_COLORS[clusterId % CLUSTER_BORDER_COLORS.length]
}

export const BRIDGE_EDGE_COLOR = '#bfbfbf'
