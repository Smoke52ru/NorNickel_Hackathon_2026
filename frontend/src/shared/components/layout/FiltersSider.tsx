import { Button, Drawer, Typography } from 'antd'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import { closeFiltersPanel } from '@/app/settingsSlice'
import { FilterControls } from '@/shared/components/filters/FilterControls'
import { useFilterForm } from '@/shared/components/filters/useFilterForm'
import type { SearchFilters } from '@/shared/types/filters'
import styles from './FiltersSider.module.css'

const { Text } = Typography

interface FiltersSiderProps {
  onApplied?: (next: SearchFilters, prev: SearchFilters) => void
}

export function FiltersSider({ onApplied }: FiltersSiderProps) {
  const dispatch = useAppDispatch()
  const open = useAppSelector((state) => state.settings.filtersPanelOpen)

  const { draft, setDraft, yearRange, setYearRange, apply, reset } =
    useFilterForm({
      syncWhenOpen: true,
      open,
      onApplied: (next, prev) => {
        onApplied?.(next, prev)
      },
    })

  const handleClose = () => {
    dispatch(closeFiltersPanel())
  }

  const handleApply = () => {
    apply()
    dispatch(closeFiltersPanel())
  }

  const handleReset = () => {
    reset()
  }

  return (
    <Drawer
      title="Фильтры"
      placement="left"
      width={360}
      open={open}
      onClose={handleClose}
      rootClassName={styles.drawer}
      footer={
        <div className={styles.footer}>
          <Button onClick={handleReset}>Сбросить</Button>
          <Button type="primary" onClick={handleApply}>
            Применить
          </Button>
        </div>
      }
    >
      <div className={styles.content}>
        <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
          Фильтры поиска и отображения графа
        </Text>
        <FilterControls
          value={draft}
          onChange={setDraft}
          yearRange={yearRange}
          onYearRangeChange={setYearRange}
        />
      </div>
    </Drawer>
  )
}
