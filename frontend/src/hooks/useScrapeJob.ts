import { useState, useEffect } from "react";
import { api } from "../lib/api";

export interface ScrapeStatus {
  job_id: string;
  status: "pending" | "scraping" | "predicting" | "done" | "failed";
  progress_message: string;
  error: string | null;
}

export function useScrapeJob() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<ScrapeStatus | null>(null);

  const startJob = async (keyword: string, targetCount: number) => {
    try {
      const res = await api.post<{ job_id: string }>("/api/v1/scrape/start", {
        keyword,
        target_count: targetCount
      });
      setJobId(res.data.job_id);
      setStatus({
        job_id: res.data.job_id,
        status: "pending",
        progress_message: "Starting job...",
        error: null
      });
    } catch (err: any) {
      setStatus({
        job_id: "",
        status: "failed",
        progress_message: "Failed to start job.",
        error: err.response?.data?.detail || err.message
      });
    }
  };

  const reset = () => {
    setJobId(null);
    setStatus(null);
  };

  useEffect(() => {
    if (!jobId) return;
    if (status?.status === "done" || status?.status === "failed") return;

    const interval = setInterval(async () => {
      try {
        const res = await api.get<ScrapeStatus>(`/api/v1/scrape/status/${jobId}`);
        setStatus(res.data);
      } catch (err) {
        console.error("Error polling status:", err);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [jobId, status?.status]);

  return { jobId, status, startJob, reset };
}
