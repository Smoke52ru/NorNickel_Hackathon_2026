import { Alert, Drawer, Empty, Spin, Typography } from 'antd'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import { closeDocumentPanel } from '@/app/settingsSlice'
import { useGetDocumentQuery } from '@/shared/api/baseApi'
import styles from './DocumentSider.module.css'

const { Text, Paragraph } = Typography

export function DocumentSider() {
  const dispatch = useAppDispatch()
  const { open, docId } = useAppSelector((state) => state.settings.documentPanel)

  const { data, isLoading, isError } = useGetDocumentQuery(docId ?? '', {
    skip: !open || !docId,
  })

  const handleClose = () => {
    dispatch(closeDocumentPanel())
  }

  return (
    <Drawer
      title={data?.title ?? 'Источник'}
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
      <div className={styles.content}>
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

        {docId && isError && (
          <Alert
            type="error"
            showIcon
            message="Не удалось загрузить документ"
            description="Документ не найден или сервер недоступен."
          />
        )}

        {docId && data && !isLoading && (
          <>
            <div className={styles.meta}>
              <Text type="secondary">Год: {data.year}</Text>
              {data.lang && <Text type="secondary">Язык: {data.lang}</Text>}
              {data.source_path && (
                <Text type="secondary" copyable={{ text: data.source_path }}>
                  Файл: {data.source_path}
                </Text>
              )}
              <Text type="secondary">ID: {data.doc_id}</Text>
            </div>
            <Paragraph className={styles.text}>{data.text}</Paragraph>
          </>
        )}
      </div>
    </Drawer>
  )
}
