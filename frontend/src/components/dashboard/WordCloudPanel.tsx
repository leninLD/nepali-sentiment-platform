import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Skeleton } from "../Skeletons";
import { EmptyWordCloudError } from "../ErrorStates";
import { api } from "../../lib/api";

const SENTIMENTS = ["all", "positive", "neutral", "negative"] as const;
type Sentiment = typeof SENTIMENTS[number];

export function WordCloudPanel({ jobId }: { jobId: string }) {
  const [activeTab, setActiveTab] = useState<Sentiment>("all");
  const [imgStatus, setImgStatus] = useState<"loading" | "ok" | "empty">("loading");

  const tabLabels: Record<Sentiment, string> = {
    all: "All",
    positive: "Positive",
    neutral: "Neutral",
    negative: "Negative",
  };

  const handleTabChange = (s: Sentiment) => {
    setActiveTab(s);
    setImgStatus("loading");
  };

  const getImageUrl = (sentiment: Sentiment) => {
    const baseUrl = api.defaults.baseURL || "http://localhost:8000";
    return `${baseUrl}/api/v1/wordcloud/${jobId}?sentiment=${sentiment}&t=${Date.now()}`;
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <span>☁️ Word Clouds</span>
          <div className="flex flex-wrap gap-1 bg-slate-100 p-1 rounded-lg text-sm">
            {SENTIMENTS.map((s) => (
              <button
                key={s}
                onClick={() => handleTabChange(s)}
                className={`px-3 py-1 rounded-md capitalize transition-colors text-sm ${
                  activeTab === s
                    ? "bg-white shadow-sm font-medium text-slate-900"
                    : "text-slate-500 hover:text-slate-800"
                }`}
              >
                {tabLabels[s]}
              </button>
            ))}
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-4 sm:p-6 bg-slate-50 rounded-b-xl">
        <div className="relative w-full max-w-3xl mx-auto aspect-[2/1] bg-white border rounded-lg overflow-hidden flex items-center justify-center">
          {/* Skeleton while loading */}
          {imgStatus === "loading" && (
            <Skeleton className="absolute inset-0 rounded-lg" />
          )}

          {imgStatus === "empty" && <EmptyWordCloudError />}

          <img
            key={activeTab}
            src={getImageUrl(activeTab)}
            alt={`${activeTab} word cloud`}
            className={`w-full h-full object-contain transition-opacity duration-300 ${imgStatus === "ok" ? "opacity-100" : "opacity-0"}`}
            onLoad={() => setImgStatus("ok")}
            onError={() => setImgStatus("empty")}
          />
        </div>
      </CardContent>
    </Card>
  );
}
