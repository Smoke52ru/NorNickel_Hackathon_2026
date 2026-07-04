const WRAP_THRESHOLD = 18

export function formatNodeLabel(label: string): string {
  const trimmed = label.trim()
  if (trimmed.length <= WRAP_THRESHOLD) return trimmed

  const mid = Math.ceil(trimmed.length / 2)
  let breakAt = -1
  let bestDistance = Infinity

  for (let i = 1; i < trimmed.length; i++) {
    const ch = trimmed[i - 1]
    if (ch === ' ' || ch === '-' || ch === '/' || ch === ',') {
      const distance = Math.abs(i - mid)
      if (distance < bestDistance) {
        bestDistance = distance
        breakAt = i
      }
    }
  }

  if (breakAt <= 0) breakAt = mid

  const firstLine = trimmed.slice(0, breakAt).trimEnd()
  const secondLine = trimmed.slice(breakAt).trimStart()

  if (!secondLine) return firstLine
  return `${firstLine}\n${secondLine}`
}
