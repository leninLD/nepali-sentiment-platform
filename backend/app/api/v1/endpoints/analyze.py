from fastapi import APIRouter, HTTPException, Request
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.ml.preprocess import clean_tweet
from app.ml.inference import predict_sentiment

router = APIRouter()

@router.post("/", response_model=AnalyzeResponse)
def analyze_text(request_data: AnalyzeRequest, request: Request):
    # Ensure model is loaded
    if not hasattr(request.app.state, "model") or not request.app.state.model:
        raise HTTPException(status_code=503, detail="Model is not loaded. Please try again later.")
    
    # Preprocess
    cleaned_text = clean_tweet(request_data.text)
    if not cleaned_text:
        # If after cleaning the text is empty, return a neutral fallback
        return AnalyzeResponse(
            label="Neutral",
            confidence_scores={"Positive": 0.0, "Neutral": 1.0, "Negative": 0.0},
            response_time_ms=0.0
        )
    
    # Inference
    try:
        label, scores, time_ms = predict_sentiment(
            text=cleaned_text,
            model=request.app.state.model,
            tokenizer=request.app.state.tokenizer,
            device=request.app.state.device
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

    return AnalyzeResponse(
        label=label,
        confidence_scores=scores,
        response_time_ms=time_ms
    )
