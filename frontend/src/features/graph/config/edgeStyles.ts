import type { EdgeFlag } from '@/shared/types/ask'

export const EDGE_STYLES: Record<
  EdgeFlag,
  { color: string; width: number; dashes: boolean }
> = {
  normal: { color: '#bfbfbf', width: 1, dashes: false },
  contradiction: { color: '#ff4d4f', width: 3, dashes: true },
  gap: { color: '#faad14', width: 3, dashes: false },
}

export const EDGE_FLAG_LABELS: Record<EdgeFlag, string> = {
  normal: 'Связь',
  contradiction: 'Противоречие',
  gap: 'Пробел',
}
