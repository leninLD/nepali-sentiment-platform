import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from app.schemas.scrape import ScrapeRequest, ScrapeStatusResponse
from app.scraping.job_manager import create_job, get_job
from app.scraping.background_worker import run_scrape_job

router = APIRouter()

@router.post("/start", response_model=dict)
def start_scrape(request_data: ScrapeRequest, background_tasks: BackgroundTasks, request: Request):
    if not hasattr(request.app.state, "model") or not request.app.state.model:
        raise HTTPException(status_code=503, detail="Model is not loaded. Cannot start job.")

    job_id = str(uuid.uuid4())
    create_job(job_id, request_data.keyword, request_data.target_count)
    
    background_tasks.add_task(
        run_scrape_job,
        job_id=job_id,
        keyword=request_data.keyword,
        target_count=request_data.target_count,
        model=request.app.state.model,
        tokenizer=request.app.state.tokenizer,
        device=request.app.state.device
    )
    
    return {"job_id": job_id}

@router.get("/status/{job_id}", response_model=ScrapeStatusResponse)
def get_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return ScrapeStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress_message=job["progress_message"],
        error=job["error"]
    )
