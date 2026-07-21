import { useState } from "react"
import { Link, useLocation } from "react-router-dom"
import { Menu, X, Brain } from "lucide-react"

const navLinks = [
  { to: "/analyzer", label: "Analyzer" },
  { to: "/scraper",  label: "Scraper"  },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/about",    label: "About"    },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const { pathname } = useLocation()

  return (
    <nav className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 items-center px-4 sm:px-8 gap-4">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 font-bold text-lg mr-4 shrink-0">
          <Brain className="w-5 h-5 text-indigo-600" />
          <span className="hidden sm:block">Nepali Sentiment AI</span>
          <span className="sm:hidden">NSentiment</span>
        </Link>

        {/* Desktop links */}
        <div className="hidden sm:flex items-center gap-1 flex-1">
          {navLinks.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                pathname === to
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
              }`}
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Mobile burger */}
        <button
          className="sm:hidden ml-auto p-2 rounded-md text-slate-600 hover:bg-slate-100"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile dropdown */}
      {open && (
        <div className="sm:hidden border-t bg-background px-4 py-3 space-y-1">
          {navLinks.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              className={`block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                pathname === to
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
              }`}
            >
              {label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}
