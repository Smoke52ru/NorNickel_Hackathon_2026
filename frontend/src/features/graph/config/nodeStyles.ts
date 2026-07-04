import type { NodeType } from '@/shared/types/ask'

export const NODE_COLORS: Record<NodeType, string> = {
  Material: '#1677ff',
  Process: '#52c41a',
  Equipment: '#722ed1',
  Property: '#fa8c16',
  Experiment: '#13c2c2',
  Publication: '#8c8c8c',
  Expert: '#eb2f96',
  Facility: '#a0522d',
}

export const NODE_TYPE_LABELS: Record<NodeType, string> = {
  Material: 'Материал',
  Process: 'Процесс',
  Equipment: 'Оборудование',
  Property: 'Свойство',
  Experiment: 'Эксперимент',
  Publication: 'Публикация',
  Expert: 'Эксперт',
  Facility: 'Объект',
}
