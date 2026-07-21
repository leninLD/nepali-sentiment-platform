"""
Job management layer using Postgres database backend.
Provides the same interface as the old in-memory JOBS dict.
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.crud import (
    create_job as db_create_job,
    get_job as db_get_job,
    update_job_status as db_update_job_status,
    add_tweet_to_job as db_add_tweet_to_job,
    get_job_as_dict,
)

# Global reference to the current DB session (set by API routes or background tasks)
_db_session: Optional[Session] = None
LATEST_JOB_ID: Optional[str] = None


def set_db_session(db: Session):
    """Set the global database session for job_manager functions."""
    global _db_session
    _db_session = db


def get_db_session() -> Session:
    """Get the current database session."""
    if _db_session is None:
        raise RuntimeError("Database session not set. Call set_db_session() first.")
    return _db_session


def create_job(job_id: str, keyword: str, target: int):
    """Create a new scrape job in the database."""
    db = get_db_session()
    db_create_job(db, job_id, keyword, target)
    global LATEST_JOB_ID
    LATEST_JOB_ID = job_id


def update_job_status(job_id: str, status: str, progress_message: str = None, error: str = None):
    """Update job status in the database."""
    db = get_db_session()
    db_update_job_status(db, job_id, status, progress_message, error)


def add_tweet_to_job(job_id: str, tweet: Dict[str, Any]):
    """Add a tweet to a job in the database."""
    db = get_db_session()
    db_add_tweet_to_job(db, job_id, tweet)


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    """Get job data as a dictionary (matching old in-memory format)."""
    db = get_db_session()
    return get_job_as_dict(db, job_id)


def get_latest_job_id() -> Optional[str]:
    """Get the ID of the most recently created job."""
    return LATEST_JOB_ID
