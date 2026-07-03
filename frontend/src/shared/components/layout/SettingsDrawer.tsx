import { useEffect, useState } from 'react'
import {
  Button,
  Checkbox,
  Divider,
  Drawer,
  Input,
  Select,
  Slider,
  Space,
  Switch,
  Typography,
} from 'antd'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import {
  closeSettingsDrawer,
  resetFilters,
  setFilters,
} from '@/app/settingsSlice'
import { NODE_TYPE_LABELS } from '@/features/graph/config/nodeStyles'
import type { NodeType } from '@/shared/types/ask'
import {
  DEFAULT_FILTERS,
  type ConfidenceFilter,
  type GeographyFilter,
  type SearchFilters,
} from '@/shared/types/filters'

const { Text } = Typography

const NODE_TYPE_OPTIONS = (
  Object.keys(NODE_TYPE_LABELS) as NodeType[]
).map((type) => ({
  label: NODE_TYPE_LABELS[type],
  value: type,
}))

const YEAR_MIN = 1990
const YEAR_MAX = 2026

export function SettingsDrawer() {
  const dispatch = useAppDispatch()
  const open = useAppSelector((state) => state.settings.settingsDrawerOpen)
  const savedFilters = useAppSelector((state) => state.settings.filters)
  const [draft, setDraft] = useState<SearchFilters>(savedFilters)
  const [yearRange, setYearRange] = useState<[number, number]>([
    savedFilters.yearFrom ?? YEAR_MIN,
    savedFilters.yearTo ?? YEAR_MAX,
  ])

  useEffect(() => {
    if (open) {
      setDraft(savedFilters)
      setYearRange([
        savedFilters.yearFrom ?? YEAR_MIN,
        savedFilters.yearTo ?? YEAR_MAX,
      ])
    }
  }, [open, savedFilters])

  const handleClose = () => {
    dispatch(closeSettingsDrawer())
  }

  const handleApply = () => {
    dispatch(
      setFilters({
        ...draft,
        yearFrom: yearRange[0] === YEAR_MIN ? null : yearRange[0],
        yearTo: yearRange[1] === YEAR_MAX ? null : yearRange[1],
      }),
    )
    dispatch(closeSettingsDrawer())
  }

  const handleReset = () => {
    setDraft(DEFAULT_FILTERS)
    setYearRange([YEAR_MIN, YEAR_MAX])
    dispatch(resetFilters())
  }

  return (
    <Drawer
      title="Настройки"
      placement="right"
      width={360}
      open={open}
      onClose={handleClose}
      footer={
        <Space style={{ width: '100%', justifyContent: 'flex-end' }}>
          <Button onClick={handleReset}>Сбросить</Button>
          <Button type="primary" onClick={handleApply}>
            Применить
          </Button>
        </Space>
      }
    >
      <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
        Фильтры поиска и отображения графа
      </Text>

      <Divider plain>
        <Text type="secondary">Поиск</Text>
      </Divider>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Типы сущностей
        </Text>
        <Checkbox.Group
          options={NODE_TYPE_OPTIONS}
          value={draft.nodeTypes}
          onChange={(values) =>
            setDraft({ ...draft, nodeTypes: values as NodeType[] })
          }
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          География
        </Text>
        <Select
          style={{ width: '100%' }}
          value={draft.geography}
          onChange={(value: GeographyFilter) =>
            setDraft({ ...draft, geography: value })
          }
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
          onChange={(value) => setYearRange(value as [number, number])}
          marks={{ [YEAR_MIN]: `${YEAR_MIN}`, [YEAR_MAX]: `${YEAR_MAX}` }}
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Минимальная достоверность
        </Text>
        <Select
          style={{ width: '100%' }}
          value={draft.minConfidence}
          onChange={(value: ConfidenceFilter) =>
            setDraft({ ...draft, minConfidence: value })
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
          value={draft.materialKeyword}
          onChange={(e) =>
            setDraft({ ...draft, materialKeyword: e.target.value })
          }
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <Text strong style={{ display: 'block', marginBottom: 8 }}>
          Процесс (ключевое слово)
        </Text>
        <Input
          placeholder="Например: электроэкстракция"
          value={draft.processKeyword}
          onChange={(e) =>
            setDraft({ ...draft, processKeyword: e.target.value })
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
            checked={draft.showContradictions}
            onChange={(checked) =>
              setDraft({ ...draft, showContradictions: checked })
            }
          />
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <Text>Показывать пробелы</Text>
          <Switch
            checked={draft.showGaps}
            onChange={(checked) =>
              setDraft({ ...draft, showGaps: checked })
            }
          />
        </div>
      </Space>
    </Drawer>
  )
}
