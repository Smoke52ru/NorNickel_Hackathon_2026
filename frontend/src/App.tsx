import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>NorNickel AI Science Hack</h1>
          <p>Knowledge Graph & Search-Analytical System</p>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function HomePage() {
  return (
    <div className="home-page">
      <h2>Welcome to the Scientific Knowledge System</h2>
      <p>This application connects articles, experiments, materials, and research data.</p>
      <div className="features">
        <div className="feature-card">
          <h3>Knowledge Graph</h3>
          <p>Visualize connections between research entities</p>
        </div>
        <div className="feature-card">
          <h3>Semantic Search</h3>
          <p>Find relevant research by meaning, not just keywords</p>
        </div>
        <div className="feature-card">
          <h3>Data Analytics</h3>
          <p>Analyze patterns and gaps in research data</p>
        </div>
      </div>
    </div>
  )
}

export default App