import { useCallback, useMemo, useState } from 'react'
import { Alert, Button } from 'antd'
import { QuestionForm } from '@/features/ask/components/QuestionForm'
import { AnswerPanel } from '@/features/ask/components/AnswerPanel'
import { useAsk } from '@/features/ask/hooks/useAsk'
import { GraphSider } from '@/shared/components/layout/GraphSider'
import { GraphEdgeTrigger } from '@/shared/components/layout/GraphEdgeTrigger'
import { FiltersSider } from '@/shared/components/layout/FiltersSider'
import { FiltersEdgeTrigger } from '@/shared/components/layout/FiltersEdgeTrigger'
import { FiltersSidebar } from '@/shared/components/filters/FiltersSidebar'
import { filterGraph } from '@/features/graph/utils/filterGraph'
import { useAppSelector } from '@/app/hooks'
import type { SearchFilters } from '@/shared/types/filters'
import { filtersNeedServerRefetch } from '@/shared/utils/filterRefetch'
import styles from './AskPage.module.css'

export function AskPage() {
  const [question, setQuestion] = useState('')
  const [hasAsked, setHasAsked] = useState(false)
  const { ask, data, isLoading, isError } = useAsk()
  const filters = useAppSelector((state) => state.settings.filters)
  const graphPanelOpen = useAppSelector((state) => state.settings.graphPanel.open)
  const filtersPanelOpen = useAppSelector(
    (state) => state.settings.filtersPanelOpen,
  )

  const filteredGraph = useMemo(
    () => filterGraph(data?.graph ?? null, filters),
    [data?.graph, filters],
  )

  const hasGraphData = (filteredGraph?.nodes.length ?? 0) > 0

  const handleFiltersApplied = useCallback(
    (next: SearchFilters, prev: SearchFilters) => {
      if (
        hasAsked &&
        question.trim() &&
        filtersNeedServerRefetch(prev, next)
      ) {
        ask(question.trim(), next)
      }
    },
    [ask, hasAsked, question],
  )

  const handleSubmit = async () => {
    if (!question.trim()) return
    setHasAsked(true)
    await ask(question.trim())
  }

  const handleRetry = () => {
    if (question.trim()) {
      ask(question.trim())
    }
  }

  return (
    <div className={styles.page}>
      <QuestionForm
        value={question}
        onChange={setQuestion}
        onSubmit={handleSubmit}
        loading={isLoading}
      />

      {isError && (
        <Alert
          type="error"
          showIcon
          message="Не удалось получить ответ"
          description="Проверьте подключение к серверу или включите режим моков (VITE_USE_MOCK=true)."
          action={
            <Button size="small" onClick={handleRetry}>
              Повторить
            </Button>
          }
          style={{ marginBottom: 16 }}
        />
      )}

      <div className={styles.mainRow}>
        <FiltersSidebar onApplied={handleFiltersApplied} />
        <div className={styles.content}>
          <AnswerPanel data={data} loading={isLoading} hasAsked={hasAsked} />
        </div>
      </div>

      <FiltersEdgeTrigger visible={!filtersPanelOpen} />

      <GraphEdgeTrigger
        visible={hasAsked && !isLoading && hasGraphData && !graphPanelOpen}
        hasGraphData={hasGraphData}
      />

      <FiltersSider onApplied={handleFiltersApplied} />

      <GraphSider
        graph={filteredGraph}
        loading={isLoading}
        hasAsked={hasAsked}
      />
    </div>
  )
}
