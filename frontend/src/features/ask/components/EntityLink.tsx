import { Typography } from 'antd'
import type { NodeType } from '@/shared/types/ask'
import { NODE_COLORS, NODE_TYPE_LABELS } from '@/features/graph/config/nodeStyles'
import styles from './EntityLink.module.css'

const { Link } = Typography

interface EntityLinkProps {
  nodeId: string
  label: string
  nodeType?: NodeType
  onClick: (nodeId: string) => void
}

export function EntityLink({
  nodeId,
  label,
  nodeType,
  onClick,
}: EntityLinkProps) {
  const color = nodeType ? NODE_COLORS[nodeType] : undefined
  const typeLabel = nodeType ? NODE_TYPE_LABELS[nodeType] : undefined

  return (
    <Link
      className={styles.link}
      onClick={(e) => {
        e.preventDefault()
        onClick(nodeId)
      }}
      title={typeLabel ? `${typeLabel}: ${label}` : label}
      style={color ? { color } : undefined}
    >
      {label}
    </Link>
  )
}
