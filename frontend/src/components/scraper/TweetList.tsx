import { useState, useEffect } from "react";
import { api } from "../../lib/api";
import { motion } from "framer-motion";
import { Card, CardContent } from "../ui/card";
import { Badge } from "../ui/badge";
import { ExternalLink } from "lucide-react";
import { TweetCardSkeleton } from "../Skeletons";
import { NoTweetsFoundError } from "../ErrorStates";

interface Tweet {
  text: string;
  url: string;
  label: string;
  confidence_scores: Record<string, number>;
}

export function TweetList({ jobId }: { jobId: string }) {
  const [tweets, setTweets] = useState<Tweet[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.get<Tweet[]>(`/api/v1/tweets/${jobId}`)
      .then(res => setTweets(res.data))
      .catch(err => setError(err.response?.data?.detail || err.message))
      .finally(() => setLoading(false));
  }, [jobId]);

  if (loading) {
    return (
      <div className="space-y-4 mt-4">
        <h3 className="font-semibold text-lg">Loading results...</h3>
        {[...Array(5)].map((_, i) => <TweetCardSkeleton key={i} />)}
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-600 text-sm">
        Failed to load tweets: {error}
      </div>
    );
  }

  if (tweets.length === 0) {
    return <NoTweetsFoundError />;
  }

  return (
    <div className="space-y-4">
      <h3 className="font-semibold text-xl">Results ({tweets.length} tweets)</h3>
      {tweets.map((tw, idx) => {
        const conf = tw.confidence_scores[tw.label];
        const isPos = tw.label.toLowerCase() === "positive";
        const isNeg = tw.label.toLowerCase() === "negative";

        return (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.04, duration: 0.25 }}
          >
            <Card className="overflow-hidden hover:shadow-sm transition-shadow">
              <CardContent className="p-4 sm:p-5 flex flex-col gap-3">
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                  <p className="text-base leading-relaxed flex-1">{tw.text}</p>
                  <Badge
                    variant={isPos ? "default" : isNeg ? "destructive" : "secondary"}
                    className={`self-start shrink-0 ${isPos ? "bg-green-500 hover:bg-green-600" : ""}`}
                  >
                    {tw.label} {conf != null ? `${Math.round(conf * 100)}%` : ""}
                  </Badge>
                </div>
                {tw.url && (
                  <a
                    href={tw.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-blue-500 hover:underline flex items-center gap-1 w-fit"
                  >
                    View original <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </CardContent>
            </Card>
          </motion.div>
        );
      })}
    </div>
  );
}
