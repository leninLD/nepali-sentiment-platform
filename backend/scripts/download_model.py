"""
Download model from Hugging Face Hub if not already present locally.
Run this at container startup to ensure the model is available.
"""

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download

def download_model_from_hub(
    repo_id: str = "xlm-roberta-base",  # Change to your actual HF model repo
    local_path: str = "./model",
    cache_dir: str = None,
):
    """
    Download model from Hugging Face Hub.
    
    Args:
        repo_id: Hugging Face repo ID (e.g., "username/nepali-sentiment-3label")
        local_path: Local directory to save the model
        cache_dir: Optional cache directory for HF downloads (defaults to ~/.cache/huggingface)
    """
    local_path = Path(local_path)
    
    # Check if model already exists locally
    if local_path.exists() and any(local_path.glob("*.safetensors")):
        print(f"✅ Model already exists at {local_path}")
        return True
    
    print(f"📥 Downloading model from Hugging Face Hub: {repo_id}")
    print(f"   Destination: {local_path}")
    
    try:
        # Create parent directories if they don't exist
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download from Hugging Face Hub
        downloaded_path = snapshot_download(
            repo_id=repo_id,
            local_dir=str(local_path),
            cache_dir=cache_dir,
            resume_download=True,
            local_files_only=False,
        )
        
        print(f"✅ Model downloaded successfully to {downloaded_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download model: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Configure these based on your actual Hugging Face model
    REPO_ID = os.getenv("HF_MODEL_REPO", "xlm-roberta-base")
    LOCAL_PATH = os.getenv("MODEL_PATH", "./model")
    
    success = download_model_from_hub(
        repo_id=REPO_ID,
        local_path=LOCAL_PATH,
    )
    
    sys.exit(0 if success else 1)
