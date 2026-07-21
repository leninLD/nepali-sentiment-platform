import { motion } from "framer-motion";
import type { ScrapeStatus } from "../../hooks/useScrapeJob";
import { Card, CardContent } from "../ui/card";

const STATUS_CONFIG: Record<string, { icon: string; bg: string; border: string }> = {
  pending:    { icon: "⏳", bg: "bg-slate-50",  border: "border-slate-200" },
  scraping:   { icon: "🌐", bg: "bg-blue-50",   border: "border-blue-200"  },
  predicting: { icon: "🧠", bg: "bg-violet-50", border: "border-violet-200"},
  done:       { icon: "✅", bg: "bg-green-50",  border: "border-green-200" },
  failed:     { icon: "❌", bg: "bg-red-50",    border: "border-red-200"   },
};

export function ScrapeProgress({ status }: { status: ScrapeStatus }) {
  const cfg = STATUS_CONFIG[status.status] ?? STATUS_CONFIG.pending;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-xl mx-auto"
    >
      <Card className={`${cfg.border} ${cfg.bg}`}>
        <CardContent className="p-6 sm:p-8 flex flex-col items-center text-center space-y-4">
          <motion.div
            className="text-4xl"
            animate={
              status.status === "scraping" || status.status === "predicting"
                ? { scale: [1, 1.15, 1] }
                : {}
            }
            transition={{ repeat: Infinity, duration: 1.5 }}
          >
            {cfg.icon}
          </motion.div>

          <div>
            <h3 className="font-semibold text-lg capitalize">{status.status}</h3>
            <p className="text-muted-foreground text-sm mt-1 max-w-sm">{status.progress_message}</p>
          </div>

          {status.error && (
            <div className="w-full text-left bg-red-100 border border-red-200 rounded-md p-3">
              <p className="text-xs font-medium text-red-700">Error detail</p>
              <p className="text-xs text-red-600 mt-0.5">{status.error}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
