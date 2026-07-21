import { useState, useEffect } from "react";
import { api } from "../lib/api";

export interface JobStats {
  total: number;
  counts: {
    Positive: number;
    Neutral: number;
    Negative: number;
  };
  percentages: {
    Positive: number;
    Neutral: number;
    Negative: number;
  };
}

export function useJobStats(jobId: string) {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<JobStats | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) return;
    
    setLoading(true);
    setError(null);
    
    api.get<JobStats>(`/api/v1/stats/${jobId}`)
      .then(res => setStats(res.data))
      .catch(err => setError(err.response?.data?.detail || err.message || "Failed to load stats"))
      .finally(() => setLoading(false));
      
  }, [jobId]);

  return { stats, loading, error };
}
