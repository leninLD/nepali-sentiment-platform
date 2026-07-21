import os
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def load_model_and_tokenizer(model_path: str):
    """
    Loads a Hugging Face XLM-RoBERTa model and tokenizer from a local directory.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model directory not found at: {model_path}")

    # Ensure we use CPU explicitly, or CUDA if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    
    model.to(device)
    model.eval()  # Set model to evaluation mode
    
    return model, tokenizer, device
