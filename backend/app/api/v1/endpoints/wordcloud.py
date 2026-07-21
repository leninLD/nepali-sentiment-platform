from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.scraping.job_manager import get_job
from app.analytics.wordcloud_gen import generate_wordcloud

router = APIRouter()

VALID_SENTIMENTS = {"all", "positive", "neutral", "negative"}


@router.get("/{job_id}")
def get_job_wordcloud(job_id: str, sentiment: str = Query("all", description="positive, neutral, negative, or all")):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    if job["status"] != "done":
        raise HTTPException(
            status_code=409,
            detail=f"Job is not finished yet (status: {job['status']}). Poll /scrape/status/{job_id} first."
        )

    sentiment = sentiment.lower()
    if sentiment not in VALID_SENTIMENTS:
        raise HTTPException(status_code=422, detail=f"sentiment must be one of {sorted(VALID_SENTIMENTS)}")

    predictions = job["tweets"]

    # Filter text based on sentiment
    filtered_texts = [
        item.get("text", "")
        for item in predictions
        if sentiment == "all" or item.get("label", "").lower() == sentiment
    ]

    # generate_wordcloud now picks its own fixed hex palette per sentiment
    # internally — pass sentiment straight through instead of a colormap name.
    buf = generate_wordcloud(filtered_texts, sentiment=sentiment)

    return StreamingResponse(buf, media_type="image/png")