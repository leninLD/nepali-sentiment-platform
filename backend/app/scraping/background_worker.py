from app.scraping.job_manager import update_job_status, add_tweet_to_job, get_job
from app.scraping.nitter_scraper import scrape_nitter
from app.ml.preprocess import clean_tweet
from app.ml.inference import predict_sentiment

def run_scrape_job(job_id: str, keyword: str, target_count: int, model, tokenizer, device):
    """
    Background worker that runs the scrape, then performs ML predictions.
    """
    def log_callback(msg: str):
        update_job_status(job_id, status="scraping", progress_message=msg)

    # 1. Scrape
    update_job_status(job_id, status="scraping", progress_message="Starting Nitter scraper...")
    try:
        raw_tweets = scrape_nitter(keyword=keyword, target=target_count, log_callback=log_callback)
    except Exception as e:
        update_job_status(job_id, status="failed", progress_message="Scraping failed", error=str(e))
        return

    if not raw_tweets:
        update_job_status(job_id, status="failed", progress_message="No tweets fetched.", error="Nitter instances down or no results.")
        return

    # 2. Predict
    update_job_status(job_id, status="predicting", progress_message=f"Predicting sentiment for {len(raw_tweets)} tweets...")
    
    for i, tw in enumerate(raw_tweets):
        text = tw["text"]
        url = tw["url"]
        date = tw.get("date")
        
        cleaned_text = clean_tweet(text)
        if not cleaned_text:
            # Fallback
            label = "Neutral"
            scores = {"Positive": 0.0, "Neutral": 1.0, "Negative": 0.0}
        else:
            try:
                label, scores, _ = predict_sentiment(cleaned_text, model, tokenizer, device)
            except Exception:
                label = "Neutral"
                scores = {"Positive": 0.0, "Neutral": 1.0, "Negative": 0.0}
        
        tweet_result = {
            "text": text,
            "url": url,
            "label": label,
            "confidence_scores": scores,
            "date": date
        }
        add_tweet_to_job(job_id, tweet_result)
        
        if i % 5 == 0:
            update_job_status(job_id, status="predicting", progress_message=f"Predicted {i+1}/{len(raw_tweets)} tweets...")

    # 3. Done
    update_job_status(job_id, status="done", progress_message=f"Successfully processed {len(raw_tweets)} tweets.")