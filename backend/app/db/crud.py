"""
CRUD operations for job and tweet storage in Postgres.
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.db.models import ScrapeJob, Tweet


def create_job(db: Session, job_id: str, keyword: str, target: int) -> ScrapeJob:
    """Create a new scrape job."""
    job = ScrapeJob(job_id=job_id, keyword=keyword, target=target)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job(db: Session, job_id: str) -> Optional[ScrapeJob]:
    """Retrieve a job by ID."""
    return db.query(ScrapeJob).filter(ScrapeJob.job_id == job_id).first()


def update_job_status(
    db: Session,
    job_id: str,
    status: str,
    progress_message: Optional[str] = None,
    error: Optional[str] = None,
) -> Optional[ScrapeJob]:
    """Update job status and optional progress message / error."""
    job = get_job(db, job_id)
    if not job:
        return None
    
    job.status = status
    if progress_message is not None:
        job.progress_message = progress_message
    if error is not None:
        job.error = error
    
    db.commit()
    db.refresh(job)
    return job


def add_tweet_to_job(db: Session, job_id: str, tweet_data: Dict[str, Any]) -> Optional[Tweet]:
    """Add a tweet to a job."""
    job = get_job(db, job_id)
    if not job:
        return None
    
    tweet = Tweet(
        job_id=job_id,
        text=tweet_data.get("text"),
        url=tweet_data.get("url"),
        label=tweet_data.get("label"),
        confidence_scores=tweet_data.get("confidence_scores"),
        date=tweet_data.get("date"),
    )
    db.add(tweet)
    db.commit()
    db.refresh(tweet)
    return tweet


def get_tweets_for_job(db: Session, job_id: str) -> List[Tweet]:
    """Get all tweets for a job."""
    return db.query(Tweet).filter(Tweet.job_id == job_id).all()


def get_job_as_dict(db: Session, job_id: str) -> Optional[Dict[str, Any]]:
    """Get job with all tweets as a dictionary (matching the old in-memory format)."""
    job = get_job(db, job_id)
    if not job:
        return None
    
    return {
        "status": job.status,
        "keyword": job.keyword,
        "target": job.target,
        "progress_message": job.progress_message,
        "error": job.error,
        "tweets": [tweet.to_dict() for tweet in job.tweets],
    }
