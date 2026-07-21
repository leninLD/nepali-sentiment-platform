import time
import torch
from typing import Dict, Tuple

def predict_sentiment(text: str, model, tokenizer, device) -> Tuple[str, Dict[str, float], float]:
    """
    Tokenizes the text, performs a forward pass, and computes confidence scores for 3 classes.
    """
    start_time = time.time()
    
    inputs = tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True, 
        max_length=512,
        padding=True
    ).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=-1).squeeze().cpu().tolist()
        
    response_time_ms = (time.time() - start_time) * 1000.0

    # Ensure probs is a list (if batch size is 1, squeeze might return a 0-dim tensor if num_classes=1, but here it's 3)
    if isinstance(probs, float):
        probs = [probs]

    id2label = getattr(model.config, "id2label", None)
    
    # Fallback default mapping for 3-class (assumed typical mapping for sentiment: Negative, Neutral, Positive)
    default_mapping = {0: "Negative", 1: "Neutral", 2: "Positive"}
    
    confidence_scores = {}
    for i, prob in enumerate(probs):
        label_name = id2label.get(i, default_mapping.get(i, f"LABEL_{i}")) if id2label else default_mapping.get(i, f"LABEL_{i}")
        confidence_scores[label_name] = round(prob, 4)
        
    predicted_idx = int(torch.argmax(logits, dim=-1).item())
    predicted_label = id2label.get(predicted_idx, default_mapping.get(predicted_idx, f"LABEL_{predicted_idx}")) if id2label else default_mapping.get(predicted_idx, f"LABEL_{predicted_idx}")

    return predicted_label, confidence_scores, response_time_ms
