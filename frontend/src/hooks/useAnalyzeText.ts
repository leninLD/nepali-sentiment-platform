import { useState } from "react";
import { api } from "../lib/api";

export interface AnalyzeResponse {
  label: string;
  confidence_scores: Record<string, number>;
  response_time_ms: number;
}

export function useAnalyzeText() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const analyze = async (text: string) => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const response = await api.post<AnalyzeResponse>("/api/v1/analyze", { text });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "Failed to analyze text");
    } finally {
      setLoading(false);
    }
  };

  return { analyze, loading, result, error };
}
