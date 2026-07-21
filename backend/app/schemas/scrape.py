from pydantic import BaseModel, Field
from typing import Optional

class ScrapeRequest(BaseModel):
    keyword: str = Field(..., description="The keyword to search for")
    target_count: int = Field(50, description="Target number of tweets to collect")

class ScrapeStatusResponse(BaseModel):
    job_id: str
    status: str
    progress_message: str
    error: Optional[str] = None
