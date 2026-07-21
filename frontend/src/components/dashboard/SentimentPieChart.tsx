import type { JobStats } from "../../hooks/useJobStats";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

export function SentimentPieChart({ stats }: { stats: JobStats }) {
  const data = [
    { name: "Positive", value: stats.percentages.Positive, color: "#22c55e" },
    { name: "Neutral", value: stats.percentages.Neutral, color: "#94a3b8" },
    { name: "Negative", value: stats.percentages.Negative, color: "#ef4444" },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Percentage Breakdown</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={5}
                dataKey="value"
                label={({ name, value }) => `${name} ${value}%`}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
