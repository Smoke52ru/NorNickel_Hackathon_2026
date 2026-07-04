import { List, Typography } from 'antd'
import type { Source } from '@/shared/types/ask'
import { useAppDispatch } from '@/app/hooks'
import { openDocumentPanel } from '@/app/settingsSlice'
import styles from './SourcesList.module.css'

const { Text, Paragraph, Link } = Typography

interface SourcesListProps {
  sources: Source[]
}

export function SourcesList({ sources }: SourcesListProps) {
  const dispatch = useAppDispatch()

  if (sources.length === 0) return null

  const handleSourceClick = (docId: string) => {
    dispatch(openDocumentPanel({ docId }))
  }

  return (
    <div className={styles.sources}>
      <Text strong>Источники</Text>
      <List
        size="small"
        dataSource={sources}
        renderItem={(source) => (
          <List.Item className={styles.sourceItem}>
            <div>
              <Link
                className={styles.titleLink}
                onClick={(e) => {
                  e.preventDefault()
                  handleSourceClick(source.doc_id)
                }}
                title="Открыть полный текст документа"
              >
                {source.title}
              </Link>
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
              <Link
                type="secondary"
                className={styles.docId}
                onClick={(e) => {
                  e.preventDefault()
                  handleSourceClick(source.doc_id)
                }}
              >
                Открыть документ "{source.title}"
              </Link>
            </div>
          </List.Item>
        )}
      />
    </div>
  )
}
