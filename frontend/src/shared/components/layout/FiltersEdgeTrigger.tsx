import { FilterOutlined } from '@ant-design/icons'
import { useAppDispatch } from '@/app/hooks'
import { openFiltersPanel } from '@/app/settingsSlice'
import styles from './FiltersEdgeTrigger.module.css'

interface FiltersEdgeTriggerProps {
  visible: boolean
}

export function FiltersEdgeTrigger({ visible }: FiltersEdgeTriggerProps) {
  const dispatch = useAppDispatch()

  if (!visible) return null

  return (
    <button
      type="button"
      className={styles.trigger}
      onClick={() => dispatch(openFiltersPanel())}
      aria-label="Открыть фильтры"
      title="Открыть фильтры"
    >
      <FilterOutlined style={{ marginBottom: 6, fontSize: 16 }} />
      Фильтры
    </button>
  )
}
