import { Outlet } from 'react-router-dom'
import styles from './AppLayout.module.css'

export function AppLayout() {
  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <h1>NorNickel AI Science Hack</h1>
        <p>Knowledge Graph & Search-Analytical System</p>
      </header>
      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}
