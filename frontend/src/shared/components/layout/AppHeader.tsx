import { Button, Tooltip } from 'antd'
import { MoonOutlined, SunOutlined } from '@ant-design/icons'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import { toggleTheme } from '@/app/settingsSlice'
import styles from './AppHeader.module.css'

export function AppHeader() {
  const dispatch = useAppDispatch()
  const themeMode = useAppSelector((state) => state.settings.theme)
  const isDark = themeMode === 'dark'

  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <span className={styles.brandName}>kickout</span>
        <span className={styles.brandTagline}>Граф знаний R&D</span>
      </div>

      <div className={styles.actions}>
        <Tooltip title={isDark ? 'Светлая тема' : 'Тёмная тема'}>
          <Button
            type="text"
            className={styles.actionBtn}
            icon={isDark ? <SunOutlined /> : <MoonOutlined />}
            onClick={() => dispatch(toggleTheme())}
            aria-label="Переключить тему"
          />
        </Tooltip>
      </div>
    </header>
  )
}
