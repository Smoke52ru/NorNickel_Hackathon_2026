import { useMemo, useState } from 'react'
import { Alert, Button } from 'antd'
import { QuestionForm } from '@/features/ask/components/QuestionForm'
import { AnswerPanel } from '@/features/ask/components/AnswerPanel'
import { useAsk } from '@/features/ask/hooks/useAsk'
import { GraphSider } from '@/shared/components/layout/GraphSider'
import { GraphEdgeTrigger } from '@/shared/components/layout/GraphEdgeTrigger'
import { filterGraph } from '@/features/graph/utils/filterGraph'
import { useAppSelector } from '@/app/hooks'
import styles from './AskPage.module.css'

export function AskPage() {
  const [question, setQuestion] = useState('')
  const [hasAsked, setHasAsked] = useState(false)
  const { ask, data, isLoading, isError } = useAsk()
  const filters = useAppSelector((state) => state.settings.filters)
  const graphPanelOpen = useAppSelector((state) => state.settings.graphPanel.open)

  const filteredGraph = useMemo(
    () => filterGraph(data?.graph ?? null, filters),
    [data?.graph, filters],
  )

  const hasGraphData = (filteredGraph?.nodes.length ?? 0) > 0

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
          style={{ marginBottom: 16, maxWidth: 960, marginInline: 'auto' }}
        />
      )}

      <div className={styles.content}>
        <AnswerPanel data={data} loading={isLoading} hasAsked={hasAsked} />
      </div>

      <GraphEdgeTrigger
        visible={hasAsked && !isLoading && hasGraphData && !graphPanelOpen}
        hasGraphData={hasGraphData}
      />

      <GraphSider
        graph={filteredGraph}
        loading={isLoading}
        hasAsked={hasAsked}
      />
    </div>
  )
}
