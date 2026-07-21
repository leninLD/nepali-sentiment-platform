from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.tweet import TweetResult
from app.scraping.job_manager import get_job

router = APIRouter()

@router.get("/{job_id}", response_model=List[TweetResult])
def get_tweets(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job["status"] not in ["done", "predicting"]:
        # Only return tweets if it's done or at least currently predicting
        return []
        
    return job["tweets"]
