from pydantic import BaseModel
from typing import Dict, Optional

class TweetResult(BaseModel):
    text: str
    url: str
    label: str
    confidence_scores: Dict[str, float]
    date: Optional[str] = None
