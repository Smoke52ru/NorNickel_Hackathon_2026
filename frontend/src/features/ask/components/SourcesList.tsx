import { List, Typography } from 'antd'
import type { Source } from '@/shared/types/ask'
import styles from './SourcesList.module.css'

const { Text, Paragraph } = Typography

interface SourcesListProps {
  sources: Source[]
}

export function SourcesList({ sources }: SourcesListProps) {
  if (sources.length === 0) return null

  return (
    <div className={styles.sources}>
      <Text strong>Источники</Text>
      <List
        size="small"
        dataSource={sources}
        renderItem={(source) => (
          <List.Item className={styles.sourceItem}>
            <div>
              <Text strong>
                {source.title}
              </Text>
              <Text type="secondary" className={styles.year}>
                {' '}
                ({source.year})
              </Text>
              <Paragraph
                type="secondary"
                className={styles.snippet}
                ellipsis={{ rows: 2, expandable: true, symbol: 'ещё' }}
              >
                {source.snippet}
              </Paragraph>
              <Text type="secondary" className={styles.docId}>
                ID: {source.doc_id}
              </Text>
            </div>
          </List.Item>
        )}
      />
    </div>
  )
}
