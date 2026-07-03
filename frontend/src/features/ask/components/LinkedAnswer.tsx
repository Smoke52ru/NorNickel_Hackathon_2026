import type { AnswerLink, GraphData } from '@/shared/types/ask'
import { useAppDispatch } from '@/app/hooks'
import { openGraphPanel } from '@/app/settingsSlice'
import { buildAnswerSegments } from '../utils/segmentAnswer'
import { EntityLink } from './EntityLink'
import styles from './LinkedAnswer.module.css'

interface LinkedAnswerProps {
  answer: string
  graph: GraphData | null
  answerLinks?: AnswerLink[]
}

export function LinkedAnswer({ answer, graph, answerLinks }: LinkedAnswerProps) {
  const dispatch = useAppDispatch()
  const segments = buildAnswerSegments(answer, graph, answerLinks)

  const handleEntityClick = (nodeId: string) => {
    dispatch(openGraphPanel({ nodeId }))
  }

  return (
    <p className={styles.answer}>
      {segments.map((segment, index) =>
        segment.type === 'entity' && segment.nodeId ? (
          <EntityLink
            key={`${segment.nodeId}-${index}`}
            nodeId={segment.nodeId}
            label={segment.text}
            nodeType={segment.nodeType}
            onClick={handleEntityClick}
          />
        ) : (
          <span key={`text-${index}`}>{segment.text}</span>
        ),
      )}
    </p>
  )
}
