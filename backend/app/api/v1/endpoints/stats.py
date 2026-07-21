from fastapi import APIRouter, HTTPException
from app.analytics.sentiment_stats import compute_stats
from app.scraping.job_manager import get_job, get_latest_job_id

router = APIRouter()

@router.get("/{job_id}")
def get_job_stats(job_id: str):
    if job_id == "demo":
        latest_job_id = get_latest_job_id()
        if latest_job_id is not None:
            job_id = latest_job_id
        else:
            raise HTTPException(status_code=404, detail="Job not found")

    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    predictions = job.get("tweets", [])

    if not predictions:
        return {
            "total": 0,
            "counts": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "percentages": {"Positive": 0, "Neutral": 0, "Negative": 0},
        }

    stats = compute_stats(predictions)
    return stats