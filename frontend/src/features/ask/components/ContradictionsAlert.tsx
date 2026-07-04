import { Alert, Typography } from 'antd'
import type { Contradiction, Source } from '@/shared/types/ask'
import { useAppDispatch } from '@/app/hooks'
import { openDocumentPanel } from '@/app/settingsSlice'
import styles from './ContradictionsAlert.module.css'

const { Text, Link } = Typography

interface ContradictionsAlertProps {
  contradictions: Contradiction[]
  sourceCatalog?: Source[]
}

export function ContradictionsAlert({
  contradictions,
  sourceCatalog = [],
}: ContradictionsAlertProps) {
  const dispatch = useAppDispatch()

  if (contradictions.length === 0) return null

  const titleByDocId = new Map(sourceCatalog.map((s) => [s.doc_id, s.title]))

  const handleSourceClick = (docId: string) => {
    dispatch(openDocumentPanel({ docId }))
  }

  return (
    <Alert
      type="error"
      showIcon
      message="Противоречия в данных"
      description={
        <ul className={styles.list}>
          {contradictions.map((c) => (
            <li key={c.about}>
              <Text strong>{c.about}</Text>
              <br />
              <Text type="secondary">Источники: </Text>
              {c.sources.map((docId, index) => (
                <span key={docId}>
                  {index > 0 && ', '}
                  <Link
                    className={styles.sourceLink}
                    onClick={(e) => {
                      e.preventDefault()
                      handleSourceClick(docId)
                    }}
                    title="Открыть полный текст документа"
                  >
                    {titleByDocId.get(docId) ?? docId}
                  </Link>
                </span>
              ))}
            </li>
          ))}
        </ul>
      }
      style={{ marginTop: 16 }}
    />
  )
}
