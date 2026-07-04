import { DocumentEdgeTrigger } from './DocumentEdgeTrigger'
import { GraphEdgeTrigger } from './GraphEdgeTrigger'
import styles from './RightEdgeTriggers.module.css'

interface RightEdgeTriggersProps {
  documentVisible: boolean
  hasSources: boolean
  graphVisible: boolean
  hasGraphData: boolean
}

export function RightEdgeTriggers({
  documentVisible,
  hasSources,
  graphVisible,
  hasGraphData,
}: RightEdgeTriggersProps) {
  if (!documentVisible && !graphVisible) return null

  return (
    <div className={styles.container}>
      <DocumentEdgeTrigger visible={documentVisible} hasSources={hasSources} />
      <GraphEdgeTrigger visible={graphVisible} hasGraphData={hasGraphData} />
    </div>
  )
}
