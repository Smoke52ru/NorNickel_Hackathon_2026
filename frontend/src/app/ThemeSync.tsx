import { useEffect } from 'react'
import { theme } from 'antd'
import { useAppSelector } from './hooks'

export function ThemeSync() {
  const themeMode = useAppSelector((state) => state.settings.theme)
  const isDark = themeMode === 'dark'
  const { token } = theme.useToken()

  useEffect(() => {
    const root = document.documentElement
    root.dataset.theme = themeMode
    root.style.colorScheme = isDark ? 'dark' : 'light'

    const cssVars: [string, string | number][] = [
      ['--ant-color-text', token.colorText],
      ['--ant-color-text-secondary', token.colorTextSecondary],
      ['--ant-color-text-tertiary', token.colorTextTertiary],
      ['--ant-color-bg-layout', token.colorBgLayout],
      ['--ant-color-bg-container', token.colorBgContainer],
      ['--ant-color-border-secondary', token.colorBorderSecondary],
      ['--ant-color-primary', token.colorPrimary],
    ]

    for (const [name, value] of cssVars) {
      root.style.setProperty(name, String(value))
    }

    document.body.style.background = token.colorBgLayout
    document.body.style.color = token.colorText
  }, [themeMode, isDark, token])

  return null
}
