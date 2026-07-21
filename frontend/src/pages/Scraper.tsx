import { PageTransition } from "../components/PageTransition";
import { useScrapeJob } from "../hooks/useScrapeJob";
import { ScrapeForm } from "../components/scraper/ScrapeForm";
import { ScrapeProgress } from "../components/scraper/ScrapeProgress";
import { TweetList } from "../components/scraper/TweetList";
import { NitterDownError, NoTweetsFoundError } from "../components/ErrorStates";
import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";

export default function Scraper() {
  const navigate = useNavigate();
  const { jobId, status, startJob, reset } = useScrapeJob();

  const isRunning = status !== null && status.status !== "done" && status.status !== "failed";
  const isDone = status?.status === "done";
  const isFailed = status?.status === "failed";

  const isNitterDown = isFailed && (
    status?.error?.toLowerCase().includes("nitter") ||
    status?.progress_message?.toLowerCase().includes("all nitter instances are down")
  );
  const isNoTweets = isFailed && (
    status?.error?.toLowerCase().includes("no tweets") ||
    status?.progress_message?.toLowerCase().includes("no nepali tweets")
  );

  return (
    <PageTransition>
      <div className="min-h-[calc(100vh-4rem)] bg-slate-50/50 px-4 py-10 sm:px-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="text-center space-y-2">
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">Live Nitter Scraper</h1>
            <p className="text-muted-foreground text-sm sm-text-base">
              Scrape live Nepali tweets — no Twitter API required — then classify them with XLM-RoBERTa.
            </p>
          </div>

          {!isRunning && !isDone && !isFailed && (
            <ScrapeForm onStart={startJob} disabled={isRunning} />
          )}

          {(isRunning || (isFailed && !isNitterDown && !isNoTweets)) && status && (
            <ScrapeProgress status={status} />
          )}

          {isNitterDown && (
            <div className="max-w-xl mx-auto">
              <NitterDownError onRetry={reset} />
              <div className="text-center mt-4">
                <Button variant="outline" onClick={reset}>Try Again</Button>
              </div>
            </div>
          )}

          {isNoTweets && (
            <div className="max-w-xl mx-auto">
              <NoTweetsFoundError keyword={status?.progress_message} />
              <div className="text-center mt-4">
                <Button variant="outline" onClick={reset}>Search Different Keyword</Button>
              </div>
            </div>
          )}

          {isDone && jobId && (
            <div className="space-y-6">
              <div className="flex justify-center gap-3">
                <Button variant="outline" onClick={reset}>Start New Scrape</Button>
                <Button onClick={() => navigate(`/dashboard?jobId=${jobId}`)}>View Dashboard</Button>
              </div>
              <TweetList jobId={jobId} />
            </div>
          )}
        </div>
      </div>
    </PageTransition>
  );
}