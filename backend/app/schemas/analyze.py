from pydantic import BaseModel, Field
from typing import Dict

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="The Nepali text to analyze")

class AnalyzeResponse(BaseModel):
    label: str = Field(..., description="The predicted sentiment label (e.g., Positive, Neutral, Negative)")
    confidence_scores: Dict[str, float] = Field(..., description="Dictionary mapping labels to confidence scores (0.0 to 1.0)")
    response_time_ms: float = Field(..., description="Inference time in milliseconds")
