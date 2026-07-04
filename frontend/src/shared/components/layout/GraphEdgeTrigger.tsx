import { ShareAltOutlined } from '@ant-design/icons'
import { useAppDispatch } from '@/app/hooks'
import { openGraphPanel } from '@/app/settingsSlice'
import { Badge } from 'antd'
import styles from './RightEdgeTriggers.module.css'


interface GraphEdgeTriggerProps {
  visible: boolean
  hasGraphData: boolean
}

export function GraphEdgeTrigger({ visible, hasGraphData }: GraphEdgeTriggerProps) {
  const dispatch = useAppDispatch()

  if (!visible) return null

  return (
    <button
      type="button"
      className={styles.trigger}
      onClick={() => dispatch(openGraphPanel())}
      aria-label="Открыть граф знаний"
      title="Открыть граф знаний"
    >
      {/* hasGraphData && <span className={styles.badge} aria-hidden /> */  }
      <Badge dot status="success" size="small" hidden={!hasGraphData}>
        <ShareAltOutlined style={{ marginBottom: 6, fontSize: 16 }} />
        Граф
      </Badge>
    </button>
  )
}
