import { Button, Card, Space } from 'antd'
import { FilterControls } from './FilterControls'
import { useFilterForm } from './useFilterForm'
import type { SearchFilters } from '@/shared/types/filters'
import styles from './FiltersSidebar.module.css'

interface FiltersSidebarProps {
  onApplied?: (next: SearchFilters, prev: SearchFilters) => void
}

export function FiltersSidebar({ onApplied }: FiltersSidebarProps) {
  const { draft, setDraft, yearRange, setYearRange, apply, reset } =
    useFilterForm({ onApplied })

  return (
    <aside className={styles.filtersSidebar}>
      <Card title="Фильтры" className={styles.card} size="small">
        <FilterControls
          value={draft}
          onChange={setDraft}
          yearRange={yearRange}
          onYearRangeChange={setYearRange}
        />
        <div className={styles.footer}>
          <Space style={{ width: '100%' }}>
            <Button onClick={reset} block>
              Сбросить
            </Button>
            <Button type="primary" onClick={apply} block>
              Применить
            </Button>
          </Space>
        </div>
      </Card>
    </aside>
  )
}
