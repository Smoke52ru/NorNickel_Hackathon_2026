import { Alert, Typography } from 'antd'
import type { Contradiction } from '@/shared/types/ask'

const { Text } = Typography

interface ContradictionsAlertProps {
  contradictions: Contradiction[]
}

export function ContradictionsAlert({ contradictions }: ContradictionsAlertProps) {
  if (contradictions.length === 0) return null

  return (
    <Alert
      type="error"
      showIcon
      message="Противоречия в данных"
      description={
        <ul style={{ margin: 0, paddingLeft: 20 }}>
          {contradictions.map((c) => (
            <li key={c.about}>
              <Text strong>{c.about}</Text>
              <br />
              <Text type="secondary">Источники: {c.sources.join(', ')}</Text>
            </li>
          ))}
        </ul>
      }
      style={{ marginTop: 16 }}
    />
  )
}
