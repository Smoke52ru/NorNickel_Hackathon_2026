import { Card, Empty, Skeleton } from 'antd'
import type { AskResponse } from '@/shared/types/ask'
import { meetsMinConfidence } from '@/shared/types/filters'
import { useAppSelector } from '@/app/hooks'
import { ConfidenceBadge } from './ConfidenceBadge'
import { SourcesList } from './SourcesList'
import { GapsAlert } from './GapsAlert'
import { ContradictionsAlert } from './ContradictionsAlert'
import { LinkedAnswer } from './LinkedAnswer'
import { LoadingOverlay } from '@/shared/components/LoadingOverlay'
import styles from './AnswerPanel.module.css'

interface AnswerPanelProps {
  data: AskResponse | null
  loading?: boolean
  hasAsked?: boolean
}

export function AnswerPanel({ data, loading = false, hasAsked = false }: AnswerPanelProps) {
  const filters = useAppSelector((state) => state.settings.filters)

  const isEmptyGap =
    data?.confidence === 'low' &&
    (!data.answer || data.answer.includes('не найдено'))

  const confidenceOk =
    !data || meetsMinConfidence(data.confidence, filters.minConfidence)

  const filteredSources =
    data?.sources.filter((source) => {
      if (filters.yearFrom !== null && source.year < filters.yearFrom) return false
      if (filters.yearTo !== null && source.year > filters.yearTo) return false
      return true
    }) ?? []

  const showLoading = loading && hasAsked
  const showInitial = !hasAsked && !loading
  const showError = hasAsked && !loading && !data

  return (
    <Card title="Ответ" className={styles.panel}>
      <LoadingOverlay loading={showLoading} tip="Анализируем запрос…">
        {showInitial && (
          <Empty description="Задайте вопрос, чтобы получить ответ" />
        )}

        {showLoading && (
          <div className={styles.skeleton}>
            <Skeleton active paragraph={{ rows: 6 }} />
          </div>
        )}

        {showError && (
          <Empty description="Не удалось получить ответ" />
        )}

        {data && !showLoading && (
          <>
            {!confidenceOk ? (
              <Empty description="Ответ не соответствует минимальному уровню достоверности" />
            ) : (
              <>
                <div className={styles.confidence}>
                  <ConfidenceBadge confidence={data.confidence} />
                </div>

                {isEmptyGap ? (
                  <Empty
                    description="Пробел в данных"
                    image={Empty.PRESENTED_IMAGE_SIMPLE}
                  />
                ) : (
                  <LinkedAnswer
                    answer={data.answer}
                    graph={data.graph}
                    answerLinks={data.answer_links}
                  />
                )}

                <SourcesList sources={filteredSources} />
                <GapsAlert gaps={data.gaps} />
                <ContradictionsAlert contradictions={data.contradictions} />
              </>
            )}
          </>
        )}
      </LoadingOverlay>
    </Card>
  )
}
