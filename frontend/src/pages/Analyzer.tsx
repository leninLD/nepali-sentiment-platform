import { PageTransition } from "../components/PageTransition";
import { TextInputCard } from "../components/analyzer/TextInputCard";
import { PredictionResult } from "../components/analyzer/PredictionResult";
import { AnalyzerResultSkeleton } from "../components/Skeletons";
import { ApiError } from "../components/ErrorStates";
import { useAnalyzeText } from "../hooks/useAnalyzeText";

export default function Analyzer() {
  const { analyze, loading, result, error } = useAnalyzeText();

  return (
    <PageTransition>
      <div className="min-h-[calc(100vh-4rem)] bg-slate-50/50 px-4 py-10 sm:px-8">
        <div className="max-w-2xl mx-auto space-y-6">
          <div className="text-center mb-8 space-y-2">
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
              Nepali Sentiment Analyzer
            </h1>
            <p className="text-muted-foreground text-sm sm:text-base">
              Test the XLM-RoBERTa model with real Nepali text to detect{" "}
              <span className="text-green-600 font-medium">Positive</span>,{" "}
              <span className="text-slate-500 font-medium">Neutral</span>, or{" "}
              <span className="text-red-500 font-medium">Negative</span> sentiment.
            </p>
          </div>

          <TextInputCard onAnalyze={analyze} loading={loading} />

          {error && (
            <ApiError
              message={error}
              onRetry={() => {}}
            />
          )}

          {loading && !result && <AnalyzerResultSkeleton />}

          {result && !loading && <PredictionResult result={result} />}
        </div>
      </div>
    </PageTransition>
  );
}
