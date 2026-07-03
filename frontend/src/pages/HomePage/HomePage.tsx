import styles from './HomePage.module.css'

export function HomePage() {
  return (
    <div className={styles.homePage}>
      <h2>Welcome to the Scientific Knowledge System</h2>
      <p>This application connects articles, experiments, materials, and research data.</p>
      <div className={styles.features}>
        <div className={styles.featureCard}>
          <h3>Knowledge Graph</h3>
          <p>Visualize connections between research entities</p>
        </div>
        <div className={styles.featureCard}>
          <h3>Semantic Search</h3>
          <p>Find relevant research by meaning, not just keywords</p>
        </div>
        <div className={styles.featureCard}>
          <h3>Data Analytics</h3>
          <p>Analyze patterns and gaps in research data</p>
        </div>
      </div>
    </div>
  )
}
