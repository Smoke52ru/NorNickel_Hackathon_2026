import styles from './AppFooter.module.css'

export function AppFooter() {
  return (
    <footer className={styles.footer}>
      <div className={styles.team}>Сделано командой kickout</div>
      <div className={styles.copyright}>© 2026 kickout. Все права защищены.</div>
    </footer>
  )
}
