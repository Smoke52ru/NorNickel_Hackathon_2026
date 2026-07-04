import type { AnswerLink, GraphData, GraphNode } from '@/shared/types/ask'

export interface AnswerSegment {
  type: 'text' | 'entity'
  text: string
  linkText?: string
  nodeId?: string
  nodeType?: GraphNode['type']
}

const WORD_CHAR = /[\p{L}\p{M}\p{N}]/u

function isWordChar(char: string): boolean {
  return char.length > 0 && WORD_CHAR.test(char)
}

/** Доводит end до конца слова, если офсет попал в середину (стеммер бэкенда). */
function extendToWordEnd(text: string, end: number, maxEnd: number): number {
  let extended = end
  while (extended < maxEnd && isWordChar(text[extended] ?? '')) {
    extended++
  }
  return extended
}

function segmentsFromLinks(
  answer: string,
  links: AnswerLink[],
  nodes: GraphNode[],
): AnswerSegment[] {
  const sorted = [...links].sort((a, b) => a.start - b.start)
  const segments: AnswerSegment[] = []
  let cursor = 0

  for (let i = 0; i < sorted.length; i++) {
    const link = sorted[i]
    const nextStart = sorted[i + 1]?.start ?? answer.length

    if (link.start < cursor || link.end > answer.length || link.start >= link.end) {
      continue
    }

    if (link.start > cursor) {
      segments.push({ type: 'text', text: answer.slice(cursor, link.start) })
    }

    const node = nodes.find((n) => n.id === link.nodeId)
    const displayEnd = extendToWordEnd(answer, link.end, nextStart)
    const linkText = answer.slice(link.start, displayEnd)

    segments.push({
      type: 'entity',
      text: link.label ?? linkText,
      linkText,
      nodeId: link.nodeId,
      nodeType: node?.type,
    })
    cursor = displayEnd
  }

  if (cursor < answer.length) {
    segments.push({ type: 'text', text: answer.slice(cursor) })
  }

  return segments.length > 0 ? segments : [{ type: 'text', text: answer }]
}

function escapeRegex(value: string): string {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function segmentsFromMatching(answer: string, nodes: GraphNode[]): AnswerSegment[] {
  const sortedNodes = [...nodes].sort(
    (a, b) => b.label.length - a.label.length,
  )

  const matches: Array<{ start: number; end: number; node: GraphNode }> = []

  for (const node of sortedNodes) {
    if (node.label.length < 3) continue

    const pattern = new RegExp(escapeRegex(node.label), 'gi')
    let match: RegExpExecArray | null

    while ((match = pattern.exec(answer)) !== null) {
      const start = match.index
      const end = start + match[0].length
      const overlaps = matches.some(
        (existing) => start < existing.end && end > existing.start,
      )
      if (!overlaps) {
        matches.push({ start, end, node })
      }
    }
  }

  matches.sort((a, b) => a.start - b.start)

  const segments: AnswerSegment[] = []
  let cursor = 0

  for (const match of matches) {
    if (match.start < cursor) continue

    if (match.start > cursor) {
      segments.push({ type: 'text', text: answer.slice(cursor, match.start) })
    }

    const linkText = answer.slice(match.start, match.end)
    segments.push({
      type: 'entity',
      text: linkText,
      linkText,
      nodeId: match.node.id,
      nodeType: match.node.type,
    })
    cursor = match.end
  }

  if (cursor < answer.length) {
    segments.push({ type: 'text', text: answer.slice(cursor) })
  }

  return segments.length > 0 ? segments : [{ type: 'text', text: answer }]
}

export function buildAnswerSegments(
  answer: string,
  graph: GraphData | null,
  answerLinks?: AnswerLink[],
): AnswerSegment[] {
  if (!graph?.nodes.length) {
    return [{ type: 'text', text: answer }]
  }

  if (answerLinks?.length) {
    return segmentsFromLinks(answer, answerLinks, graph.nodes)
  }

  return segmentsFromMatching(answer, graph.nodes)
}
