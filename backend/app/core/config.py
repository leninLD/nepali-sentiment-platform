from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nepali Sentiment Platform API"
    API_V1_STR: str = "/api/v1"
    
    # Model configuration
    MODEL_PATH: str = "./model"
    HF_MODEL_REPO: str = "xlm-roberta-base"  # Change to your actual HF repo (e.g., "username/nepali-sentiment-3label")
    
    # CORS configuration
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ]
    
    # Database configuration
    DATABASE_URL: str = "sqlite:///./test.db"  # Override with DATABASE_URL env var on Render (e.g., postgresql://...)

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", env_file_encoding="utf-8")

settings = Settings()
