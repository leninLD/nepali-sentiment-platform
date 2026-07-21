import type { JobStats } from "../../hooks/useJobStats";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface StatCardProps {
  label: string;
  icon: string;
  value: number | string;
  sub?: string;
  valueClass?: string;
}

function StatCard({ label, icon, value, sub, valueClass = "" }: StatCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{label}</CardTitle>
        <span className="text-xl">{icon}</span>
      </CardHeader>
      <CardContent>
        <div className={`text-2xl font-bold ${valueClass}`}>{value}</div>
        {sub && <p className="text-xs text-muted-foreground mt-0.5">{sub}</p>}
      </CardContent>
    </Card>
  );
}

export function StatSummaryCards({ stats }: { stats: JobStats }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard
        label="Total Tweets"
        icon="📊"
        value={stats.total}
      />
      <StatCard
        label="Positive"
        icon="✅"
        value={stats.counts.Positive}
        sub={`${stats.percentages.Positive}% of total`}
        valueClass="text-green-600"
      />
      <StatCard
        label="Neutral"
        icon="➖"
        value={stats.counts.Neutral}
        sub={`${stats.percentages.Neutral}% of total`}
        valueClass="text-slate-500"
      />
      <StatCard
        label="Negative"
        icon="❌"
        value={stats.counts.Negative}
        sub={`${stats.percentages.Negative}% of total`}
        valueClass="text-red-600"
      />
    </div>
  );
}
