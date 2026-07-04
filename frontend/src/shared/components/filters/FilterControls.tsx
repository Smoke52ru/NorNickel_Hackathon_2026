import {
  Checkbox,
  Divider,
  Input,
  Select,
  Slider,
  Space,
  Switch,
  Typography,
} from 'antd'
import { NODE_TYPE_LABELS } from '@/features/graph/config/nodeStyles'
import type { NodeType } from '@/shared/types/ask'
import type {
  ConfidenceFilter,
  GeographyFilter,
  SearchFilters,
} from '@/shared/types/filters'

const { Text } = Typography

export const YEAR_MIN = 1990
export const YEAR_MAX = 2026

const NODE_TYPE_OPTIONS = (
  Object.keys(NODE_TYPE_LABELS) as NodeType[]
).map((type) => ({
  label: NODE_TYPE_LABELS[type],
  value: type,
}))

export interface FilterControlsProps {
  value: SearchFilters
  onChange: (next: SearchFilters) => void
  yearRange: [number, number]
  onYearRangeChange: (range: [number, number]) => void
}

export function FilterControls({
  value,
  onChange,
  yearRange,
  onYearRangeChange,
}: FilterControlsProps) {
  return (
    <>
      <Divider plain>
        <Text type="secondary">Поиск</Text>
      </Divider>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Типы сущностей
        </Text>
        <Checkbox.Group
          options={NODE_TYPE_OPTIONS}
          value={value.nodeTypes}
          onChange={(values) =>
            onChange({ ...value, nodeTypes: values as NodeType[] })
          }
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          География
        </Text>
        <Select
          style={{ width: '100%' }}
          value={value.geography}
          onChange={(geo: GeographyFilter) => onChange({ ...value, geography: geo })}
          options={[
            { label: 'Вся практика', value: 'all' },
            { label: 'Отечественная', value: 'domestic' },
            { label: 'Зарубежная', value: 'foreign' },
          ]}
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Год публикации
        </Text>
        <Slider
          range
          min={YEAR_MIN}
          max={YEAR_MAX}
          value={yearRange}
          onChange={(range) => onYearRangeChange(range as [number, number])}
          marks={{ [YEAR_MIN]: `${YEAR_MIN}`, [YEAR_MAX]: `${YEAR_MAX}` }}
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Минимальная достоверность
        </Text>
        <Select
          style={{ width: '100%' }}
          value={value.minConfidence}
          onChange={(minConfidence: ConfidenceFilter) =>
            onChange({ ...value, minConfidence })
          }
          options={[
            { label: 'Низкая и выше', value: 'low' },
            { label: 'Средняя и выше', value: 'medium' },
            { label: 'Только высокая', value: 'high' },
          ]}
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Материал (ключевое слово)
        </Text>
        <Input
          placeholder="Например: никель"
          value={value.materialKeyword}
          onChange={(e) =>
            onChange({ ...value, materialKeyword: e.target.value })
          }
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Процесс (ключевое слово)
        </Text>
        <Input
          placeholder="Например: электроэкстракция"
          value={value.processKeyword}
          onChange={(e) =>
            onChange({ ...value, processKeyword: e.target.value })
          }
        />
      </div>

      <Divider plain>
        <Text type="secondary">Граф</Text>
      </Divider>

      <Space direction="vertical" style={{ width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <Text>Показывать противоречия</Text>
          <Switch
            checked={value.showContradictions}
            onChange={(checked) =>
              onChange({ ...value, showContradictions: checked })
            }
          />
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <Text>Показывать пробелы</Text>
          <Switch
            checked={value.showGaps}
            onChange={(checked) => onChange({ ...value, showGaps: checked })}
          />
        </div>
      </Space>
    </>
  )
}
