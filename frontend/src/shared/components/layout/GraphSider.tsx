import { Drawer } from 'antd'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import { closeGraphPanel } from '@/app/settingsSlice'
import { KnowledgeGraph } from '@/features/graph/components/KnowledgeGraph'
import type { GraphData } from '@/shared/types/ask'
import styles from './GraphSider.module.css'

interface GraphSiderProps {
  graph: GraphData | null
  loading?: boolean
  hasAsked?: boolean
}

export function GraphSider({
  graph,
  loading = false,
  hasAsked = false,
}: GraphSiderProps) {
  const dispatch = useAppDispatch()
  const { open, focusedNodeId } = useAppSelector((state) => state.settings.graphPanel)

  return (
    <Drawer
      title="Граф знаний"
      placement="right"
      width={720}
      open={open}
      onClose={() => dispatch(closeGraphPanel())}
      destroyOnClose={false}
      rootClassName={styles.drawer}
      styles={{
        section: { height: '100%' },
        body: {
          padding: 0,
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        },
      }}
    >
      <div className={styles.graphWrapper}>
        <KnowledgeGraph
          graph={graph}
          loading={loading}
          hasAsked={hasAsked}
          focusedNodeId={focusedNodeId}
          panelOpen={open}
          embedded
        />
      </div>
    </Drawer>
  )
}
