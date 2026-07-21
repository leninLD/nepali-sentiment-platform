import pandas as pd

def compute_stats(predictions: list[dict]) -> dict:
    """
    Computes count and percentage statistics for Positive, Neutral, and Negative labels.
    Expected input format:
    [
        {"text": "...", "label": "Positive", "confidence": 0.9},
        {"text": "...", "label": "Negative", "confidence": 0.8},
        ...
    ]
    """
    if not predictions:
        return {
            "total": 0,
            "counts": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "percentages": {"Positive": 0.0, "Neutral": 0.0, "Negative": 0.0}
        }

    df = pd.DataFrame(predictions)
    
    # Normalize labels to Title Case to ensure consistency
    if "label" in df.columns:
        df["label"] = df["label"].str.title()
    else:
        df["label"] = "Neutral"

    total = len(df)
    
    counts = {
        "Positive": int((df["label"] == "Positive").sum()),
        "Neutral": int((df["label"] == "Neutral").sum()),
        "Negative": int((df["label"] == "Negative").sum())
    }

    percentages = {
        "Positive": round((counts["Positive"] / total) * 100, 2) if total > 0 else 0.0,
        "Neutral": round((counts["Neutral"] / total) * 100, 2) if total > 0 else 0.0,
        "Negative": round((counts["Negative"] / total) * 100, 2) if total > 0 else 0.0
    }

    return {
        "total": total,
        "counts": counts,
        "percentages": percentages
    }
