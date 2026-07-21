"""
SQLAlchemy ORM models for job and tweet storage.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


class ScrapeJob(Base):
    """Model for storing scrape job metadata."""
    
    __tablename__ = "scrape_jobs"
    
    job_id = Column(String(255), primary_key=True, index=True)
    keyword = Column(String(255), nullable=False)
    target = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="pending")  # pending, scraping, predicting, done, failed
    progress_message = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship to tweets
    tweets = relationship("Tweet", back_populates="job", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "job_id": self.job_id,
            "keyword": self.keyword,
            "target": self.target,
            "status": self.status,
            "progress_message": self.progress_message,
            "error": self.error,
            "tweets": [tweet.to_dict() for tweet in self.tweets],
        }


class Tweet(Base):
    """Model for storing individual tweet predictions."""
    
    __tablename__ = "tweets"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(255), ForeignKey("scrape_jobs.job_id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    url = Column(Text, nullable=True)
    label = Column(String(50), nullable=False)  # Positive, Neutral, Negative
    confidence_scores = Column(JSON, nullable=False)  # {"Positive": 0.5, "Neutral": 0.3, "Negative": 0.2}
    date = Column(String(50), nullable=True)  # ISO 8601 datetime string or null
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship to job
    job = relationship("ScrapeJob", back_populates="tweets")
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "text": self.text,
            "url": self.url,
            "label": self.label,
            "confidence_scores": self.confidence_scores,
            "date": self.date,
        }
