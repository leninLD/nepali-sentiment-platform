import { useEffect, useState } from "react";
import type { JobStats } from "../../hooks/useJobStats";
import { api } from "../../lib/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

function formatTweetDate(value: string | null | undefined) {
  if (!value) return null;

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return null;

  const year = parsed.getUTCFullYear();
  const month = parsed.getUTCMonth() + 1;
  const day = parsed.getUTCDate();
  return `${year}-${month}-${day}`;
}

function TweetDateRange({ jobId }: { jobId: string }) {
  const [rangeText, setRangeText] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;

    let isMounted = true;

    api.get<Array<{ date?: string | null }>>(`/api/v1/tweets/${jobId}`)
      .then((res) => {
        if (!isMounted) return;

        const validDates = (res.data || [])
          .map((tweet) => {
            const value = tweet.date ?? null;
            if (!value) return null;

            const parsed = new Date(value);
            if (Number.isNaN(parsed.getTime())) return null;

            return {
              raw: value,
              formatted: formatTweetDate(value),
              timestamp: parsed.getTime(),
            };
          })
          .filter((entry): entry is { raw: string; formatted: string; timestamp: number } => Boolean(entry));

        if (validDates.length === 0) {
          setRangeText(null);
          return;
        }

        const oldest = validDates.reduce((earliest, current) => current.timestamp < earliest.timestamp ? current : earliest);
        const newest = validDates.reduce((latest, current) => current.timestamp > latest.timestamp ? current : latest);
        setRangeText(`Tweets collected from ${oldest.formatted} to ${newest.formatted}`);
      })
      .catch(() => {
        if (isMounted) {
          setRangeText(null);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [jobId]);

  if (!rangeText) return null;

  return (
    <div className="mb-4 rounded-lg border border-slate-200 bg-slate-50/70 px-3 py-2 text-sm text-slate-600">
      {rangeText}
    </div>
  );
}

export function SentimentBarChart({ stats, jobId }: { stats: JobStats; jobId: string }) {
  const data = [
    { name: "Positive", count: stats.counts.Positive, color: "#22c55e" },
    { name: "Neutral", count: stats.counts.Neutral, color: "#94a3b8" },
    { name: "Negative", count: stats.counts.Negative, color: "#ef4444" },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Sentiment Distribution</CardTitle>
      </CardHeader>
      <CardContent>
        <TweetDateRange jobId={jobId} />
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip cursor={{ fill: 'transparent' }} />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
