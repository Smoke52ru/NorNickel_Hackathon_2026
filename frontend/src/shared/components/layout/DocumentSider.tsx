import { Alert, Drawer, Empty, Spin, Typography } from 'antd'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import { closeDocumentPanel } from '@/app/settingsSlice'
import { useGetDocumentQuery } from '@/shared/api/baseApi'
import type { ReactNode } from 'react'
import type { Mention } from '@/shared/types/document'
import styles from './DocumentSider.module.css'

const { Text, Paragraph } = Typography

function renderText(text: string, mentions?: Mention[]): ReactNode {
  if (!mentions?.length) return text
  const spans = [...mentions].filter((m) => m.end > m.start).sort((a, b) => a.start - b.start)
  const parts: ReactNode[] = []
  let cursor = 0
  spans.forEach((m, i) => {
    if (m.start < cursor) return
    if (m.start > cursor) parts.push(text.slice(cursor, m.start))
    parts.push(
      <mark
        key={i}
        data-node-id={m.nodeId}
        title={m.label ?? m.nodeId}
        style={{ background: '#fff3bf', color: 'inherit', padding: '0 1px', borderRadius: 2 }}
      >
        {text.slice(m.start, m.end)}
      </mark>,
    )
    cursor = m.end
  })
  if (cursor < text.length) parts.push(text.slice(cursor))
  return parts
}

export function DocumentSider() {
  const dispatch = useAppDispatch()
  const { open, docId } = useAppSelector((state) => state.settings.documentPanel)

  const { currentData, isLoading, isError } = useGetDocumentQuery(docId!, {
    skip: !open || !docId,
  })

  const handleClose = () => {
    dispatch(closeDocumentPanel())
  }

  return (
    <Drawer
      title={currentData?.title ?? 'Источник'}
      placement="right"
      width={560}
      open={open}
      onClose={handleClose}
      destroyOnClose={false}
      rootClassName={styles.drawer}
      styles={{
        section: { height: '100%' },
        body: {
          padding: '0 24px 24px',
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
        },
      }}
    >
      <div key={docId ?? 'empty'} className={styles.content}>
        {!docId && (
          <div className={styles.empty}>
            <Empty description="Выберите источник из списка в ответе" />
          </div>
        )}

        {docId && isLoading && (
          <div className={styles.loading}>
            <Spin tip="Загружаем документ…" />
          </div>
        )}

        {docId && isError && !isLoading && (
          <Alert
            type="error"
            showIcon
            message="Не удалось загрузить документ"
            description="Документ не найден или сервер недоступен."
          />
        )}

        {docId && currentData && !isLoading && (
          <>
            <div className={styles.meta}>
              <Text type="secondary">Год: {currentData.year}</Text>
              {currentData.lang && <Text type="secondary">Язык: {currentData.lang}</Text>}
              {currentData.source_path && (
                <Text type="secondary" copyable={{ text: currentData.source_path }}>
                  Файл: {currentData.source_path}
                </Text>
              )}
              <Text type="secondary">ID: {currentData.doc_id}</Text>
            </div>
            <Paragraph className={styles.text} style={{ whiteSpace: 'pre-wrap' }}>
              {renderText(currentData.text, currentData.mentions)}
            </Paragraph>
          </>
        )}
      </div>
    </Drawer>
  )
}
