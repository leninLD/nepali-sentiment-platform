# Dummy storage mapping a job_id to a list of scraped & predicted tweets
# In a real app, this would be fetched from a database (e.g., PostgreSQL or SQLite)

MOCK_JOBS = {
    "demo": [
        {"text": "नेपाल सरकारले राम्रो काम गर्दैछ।", "label": "Positive", "confidence": 0.95},
        {"text": "आजको मौसम कति राम्रो छ।", "label": "Positive", "confidence": 0.88},
        {"text": "यो बाटो एकदमै खराब छ, कहिले बन्छ?", "label": "Negative", "confidence": 0.92},
        {"text": "भ्रष्टाचारले देश बर्बाद भयो।", "label": "Negative", "confidence": 0.98},
        {"text": "मलाई आज एकदम दुख लाग्यो।", "label": "Negative", "confidence": 0.85},
        {"text": "आज मंगलबार हो।", "label": "Neutral", "confidence": 0.99},
        {"text": "म बजार जाँदै छु।", "label": "Neutral", "confidence": 0.90},
        {"text": "मलाई यो मन पर्यो।", "label": "Positive", "confidence": 0.91},
        {"text": "यसको मूल्य १०० रुपैयाँ हो।", "label": "Neutral", "confidence": 0.87},
        {"text": "हाम्रो देशको विकास कहिले होला?", "label": "Negative", "confidence": 0.75},
    ]
}
