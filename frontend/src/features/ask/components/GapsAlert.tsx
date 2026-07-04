import { Alert } from 'antd'

interface GapsAlertProps {
  gaps: string[]
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
            <li key={gap}>{gap}</li>
          ))}
        </ul>
      }
      style={{ marginTop: 16 }}
    />
  )
}
