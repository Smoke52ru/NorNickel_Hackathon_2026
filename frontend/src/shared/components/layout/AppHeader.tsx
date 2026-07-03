import { Button, Tooltip, theme } from 'antd'
import {
  MoonOutlined,
  SettingOutlined,
  SunOutlined,
} from '@ant-design/icons'
import { useAppDispatch, useAppSelector } from '@/app/hooks'
import { openSettingsDrawer, toggleTheme } from '@/app/settingsSlice'
import styles from './AppHeader.module.css'

export function AppHeader() {
  const dispatch = useAppDispatch()
  const themeMode = useAppSelector((state) => state.settings.theme)
  const isDark = themeMode === 'dark'
  const { token } = theme.useToken()

  return (
    <header
      className={styles.header}
      style={{
        backgroundColor: token.colorBgContainer,
        borderBottomColor: token.colorBorderSecondary,
      }}
    >
      <div className={styles.brand}>
        <span className={styles.brandName}>kickout</span>
        <span className={styles.brandTagline}>Граф знаний R&D</span>
      </div>

      <div className={styles.actions}>
        <Tooltip title={isDark ? 'Светлая тема' : 'Тёмная тема'}>
          <Button
            type="text"
            icon={isDark ? <SunOutlined /> : <MoonOutlined />}
            onClick={() => dispatch(toggleTheme())}
            aria-label="Переключить тему"
          />
        </Tooltip>
        <Tooltip title="Настройки">
          <Button
            type="text"
            icon={<SettingOutlined />}
            onClick={() => dispatch(openSettingsDrawer())}
            aria-label="Открыть настройки"
          />
        </Tooltip>
      </div>
    </header>
  )
}
