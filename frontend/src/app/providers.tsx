import type { ReactNode } from 'react'
import { Provider } from 'react-redux'
import { ConfigProvider, theme as antTheme } from 'antd'
import ruRU from 'antd/locale/ru_RU'
import { store } from './store'
import { useAppSelector } from './hooks'
import { ThemeSync } from './ThemeSync'

const { defaultAlgorithm, darkAlgorithm } = antTheme

interface ProvidersProps {
  children: ReactNode
}

function AntdProvider({ children }: ProvidersProps) {
  const themeMode = useAppSelector((state) => state.settings.theme)
  const isDark = themeMode === 'dark'

  return (
    <ConfigProvider
      locale={ruRU}
      theme={{
        algorithm: isDark ? darkAlgorithm : defaultAlgorithm,
        token: {
          colorPrimary: '#1677ff',
          colorBgLayout: isDark ? '#0a0a0a' : '#f0f2f5',
          colorBgContainer: isDark ? '#141414' : '#ffffff',
        },
      }}
    >
      <ThemeSync />
      {children}
    </ConfigProvider>
  )
}

export function Providers({ children }: ProvidersProps) {
  return (
    <Provider store={store}>
      <AntdProvider>{children}</AntdProvider>
    </Provider>
  )
}
