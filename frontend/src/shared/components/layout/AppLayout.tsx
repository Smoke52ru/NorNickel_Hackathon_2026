import { Outlet } from 'react-router-dom'
import { AppHeader } from './AppHeader'
import { AppFooter } from './AppFooter'
import { SettingsDrawer } from './SettingsDrawer'
import styles from './AppLayout.module.css'

export function AppLayout() {
  return (
    <div className={styles.app}>
      <AppHeader />
      <main className={styles.main}>
        <Outlet />
      </main>
      <AppFooter />
      <SettingsDrawer />
    </div>
  )
}
