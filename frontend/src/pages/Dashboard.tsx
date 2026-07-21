import { PageTransition } from "../components/PageTransition";
import { StatSummaryCards } from "../components/dashboard/StatSummaryCards";
import { SentimentBarChart } from "../components/dashboard/SentimentBarChart";
import { SentimentPieChart } from "../components/dashboard/SentimentPieChart";
import { WordCloudPanel } from "../components/dashboard/WordCloudPanel";
import { StatCardSkeleton, ChartSkeleton } from "../components/Skeletons";
import { ApiError } from "../components/ErrorStates";
import { useJobStats } from "../hooks/useJobStats";
import { useLocation } from "react-router-dom";

export default function Dashboard() {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const jobId = searchParams.get("jobId") || "demo";
  const { stats, loading, error } = useJobStats(jobId);

  return (
    <PageTransition>
      <div className="min-h-[calc(100vh-4rem)] bg-slate-50/50 px-4 py-10 sm:px-8">
        <div className="max-w-6xl mx-auto space-y-8">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">Analytics Dashboard</h1>
            <p className="text-muted-foreground mt-1 text-sm">
              Overview for job{" "}
              <code className="font-mono bg-slate-200 px-1.5 py-0.5 rounded text-xs">{jobId}</code>
            </p>
          </div>

          {error && (
            <ApiError message={error} />
          )}

          {loading && !stats && (
            <div className="space-y-6">
              <StatCardSkeleton />
              <div className="grid sm:grid-cols-2 gap-4">
                <ChartSkeleton />
                <ChartSkeleton />
              </div>
            </div>
          )}

          {stats && (
            <div className="space-y-6">
              <StatSummaryCards stats={stats} />
              <div className="grid sm:grid-cols-2 gap-4">
                <SentimentBarChart stats={stats} jobId={jobId} />
                <SentimentPieChart stats={stats} />
              </div>
              <WordCloudPanel jobId={jobId} />
            </div>
          )}
        </div>
      </div>
    </PageTransition>
  );
}