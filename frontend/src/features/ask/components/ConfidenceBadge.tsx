import { Tag } from 'antd'
import type { Confidence } from '@/shared/types/ask'

const CONFIDENCE_CONFIG: Record<
  Confidence,
  { label: string; color: string }
> = {
  high: { label: 'Высокая уверенность', color: 'success' },
  medium: { label: 'Средняя уверенность', color: 'warning' },
  low: { label: 'Низкая уверенность', color: 'error' },
}

interface ConfidenceBadgeProps {
  confidence: Confidence
}

export function ConfidenceBadge({ confidence }: ConfidenceBadgeProps) {
  const { label, color } = CONFIDENCE_CONFIG[confidence]
  return <Tag color={color}>{label}</Tag>
}
