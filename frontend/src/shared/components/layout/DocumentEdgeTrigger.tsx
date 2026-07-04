import { FileTextOutlined } from '@ant-design/icons'
import { useAppDispatch } from '@/app/hooks'
import { openDocumentPanel } from '@/app/settingsSlice'
import { Badge } from 'antd'
import styles from './RightEdgeTriggers.module.css'

interface DocumentEdgeTriggerProps {
  visible: boolean
  hasSources: boolean
}

export function DocumentEdgeTrigger({
  visible,
  hasSources,
}: DocumentEdgeTriggerProps) {
  const dispatch = useAppDispatch()

  if (!visible) return null

  return (
    <button
      type="button"
      className={styles.trigger}
      onClick={() => dispatch(openDocumentPanel())}
      aria-label="Открыть панель источников"
      title="Открыть панель источников"
    >
      {/* hasSources && <span className={styles.badge} aria-hidden /> */}
      <Badge dot status="success" size="small" hidden={!hasSources}>
        <FileTextOutlined style={{ marginBottom: 6, fontSize: 16 }} />
        Источник
      </Badge>
    </button>
  )
}
