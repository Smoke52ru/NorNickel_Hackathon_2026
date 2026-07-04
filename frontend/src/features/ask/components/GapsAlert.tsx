import { Alert, Typography } from 'antd'
import type { Gap } from '@/shared/types/ask'

const { Text } = Typography

interface GapsAlertProps {
  gaps: Gap[]
}

export function GapsAlert({ gaps }: GapsAlertProps) {
  if (gaps.length === 0) return null

  return (
    <Alert
      type="warning"
      showIcon
      message="Пробелы в данных"
      description={
        <ul style={{ margin: 0, paddingLeft: 20 }}>
          {gaps.map((gap) => (
            <li key={`${gap.material}-${gap.process}`}>
              <Text strong>
                {gap.material} × {gap.process}
              </Text>
              <br />
              <Text type="secondary">{gap.reason}</Text>
            </li>
          ))}
        </ul>
      }
      style={{ marginTop: 16 }}
    />
  )
}
