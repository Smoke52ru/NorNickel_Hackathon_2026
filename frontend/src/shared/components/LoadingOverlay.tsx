import type { ReactNode } from 'react'
import { Spin } from 'antd'
import styles from './LoadingOverlay.module.css'

interface LoadingOverlayProps {
  loading: boolean
  tip?: string
  children: ReactNode
  className?: string
  fill?: boolean
}

export function LoadingOverlay({
  loading,
  tip = 'Загрузка…',
  children,
  className,
  fill = false,
}: LoadingOverlayProps) {
  return (
    <div
      className={`${styles.wrapper} ${fill ? styles.fill : ''} ${className ?? ''}`}
    >
      <div
        className={`${styles.content} ${loading ? styles.contentLoading : ''}`}
      >
        {children}
      </div>
      {loading && (
        <div className={styles.overlay}>
          <Spin size="large" tip={tip} />
        </div>
      )}
    </div>
  )
}
