import matplotlib
matplotlib.use("Agg")

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.ml.model_loader import load_model_and_tokenizer
from app.db.database import engine, SessionLocal
from app.db.models import Base
from app.scraping.job_manager import set_db_session

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database, download model, and load it
    try:
        # Create database tables
        logger.info("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created or verified.")
        
        # Set up database session for job_manager
        db = SessionLocal()
        set_db_session(db)
        logger.info("Database session initialized for job manager.")
        
        # Download model from Hugging Face if not present locally
        logger.info(f"Checking model at {settings.MODEL_PATH}...")
        if not os.path.exists(settings.MODEL_PATH) or not any(
            f.endswith(".safetensors") for f in os.listdir(settings.MODEL_PATH)
        ):
            logger.info(f"Downloading model from Hugging Face Hub: {settings.HF_MODEL_REPO}")
            from scripts.download_model import download_model_from_hub
            success = download_model_from_hub(
                repo_id=settings.HF_MODEL_REPO,
                local_path=settings.MODEL_PATH,
            )
            if not success:
                logger.error("Failed to download model from Hugging Face Hub")
                app.state.model = None
                app.state.tokenizer = None
                app.state.device = None
                yield
                return
        
        # Load the model
        logger.info(f"Loading model from {settings.MODEL_PATH}...")
        model, tokenizer, device = load_model_and_tokenizer(settings.MODEL_PATH)
        app.state.model = model
        app.state.tokenizer = tokenizer
        app.state.device = device
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize app: {e}")
        app.state.model = None
        app.state.tokenizer = None
        app.state.device = None
    
    yield
    
    # Shutdown: Clean up
    app.state.model = None
    app.state.tokenizer = None
    app.state.device = None

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware with actual origins from config
if isinstance(settings.CORS_ORIGINS, str):
    cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
else:
    cors_origins = settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {"status": "ok"}

@app.get(f"{settings.API_V1_STR}/ready")
def readiness_check():
    if getattr(app.state, "model", None) is not None:
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Model not loaded")

from app.api.v1.endpoints import analyze, stats, wordcloud, scrape, tweets

# Include routers
app.include_router(analyze.router, prefix=f"{settings.API_V1_STR}/analyze", tags=["analyze"])
app.include_router(stats.router, prefix=f"{settings.API_V1_STR}/stats", tags=["stats"])
app.include_router(wordcloud.router, prefix=f"{settings.API_V1_STR}/wordcloud", tags=["wordcloud"])
app.include_router(scrape.router, prefix=f"{settings.API_V1_STR}/scrape", tags=["scrape"])
app.include_router(tweets.router, prefix=f"{settings.API_V1_STR}/tweets", tags=["tweets"])

