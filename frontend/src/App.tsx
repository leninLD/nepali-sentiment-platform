import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom"
import { AnimatePresence } from "framer-motion"
import Navbar from "./components/Navbar"
import Analyzer from "./pages/Analyzer"
import Scraper from "./pages/Scraper"
import Dashboard from "./pages/Dashboard"
import About from "./pages/About"

function AnimatedRoutes() {
  const location = useLocation()
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Navigate to="/analyzer" replace />} />
        <Route path="/analyzer" element={<Analyzer />} />
        <Route path="/scraper" element={<Scraper />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </AnimatePresence>
  )
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background font-sans antialiased">
        <Navbar />
        <main>
          <AnimatedRoutes />
        </main>
      </div>
    </Router>
  )
}

export default App
