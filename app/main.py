# app/main.py
import logging
from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from .models import TextRequest, ErrorResponse
from .llm_service import llm_service
from .storage import storage
from .business_logic import BusinessLogic

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize business logic
business_logic = BusinessLogic(storage)

app = FastAPI(
    title="LLM Text Processor API",
    description="A RESTful API for processing text using LLMs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "details": str(exc)},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "details": str(exc)},
    )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "api": "LLM Text Processor",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/process", "method": "POST", "description": "Process text with LLM"},
            {"path": "/history", "method": "GET", "description": "Get processing history"},
            {"path": "/stats", "method": "GET", "description": "Get processing statistics"},
            {"path": "/recent-activity/{hours}", "method": "GET", "description": "Get recent activity"},
            {"path": "/sentiment-distribution", "method": "GET", "description": "Get sentiment distribution"},
            {"path": "/health", "method": "GET", "description": "Health check"}
        ]
    }

@app.post("/process", status_code=200)
async def process_text(
    request: TextRequest,
    task: str = Query("summarize", description="Processing task: summarize, entities, or sentiment")
):
    """Process text using an LLM based on the specified task"""
    logger.info(f"Processing text with task: {task}")
    try:
        # Validate task type
        if task not in ["summarize", "entities", "sentiment"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid task: {task}. Must be one of: summarize, entities, sentiment"
            )
        
        # Process the text with LLM
        processed_result = llm_service.process_text(request.text, task)
        
        # Save the result
        saved_result = storage.save_result(
            original_text=request.text,
            processed_result=processed_result,
            task_type=task
        )
        
        logger.info(f"Successfully processed text. Result ID: {saved_result['id']}")
        return saved_result
        
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text: {str(e)}"
        )

@app.get("/history")
async def get_processing_history():
    """Retrieve all processed text results"""
    return storage.get_all_results()

@app.get("/stats")
async def get_stats():
    """Get statistics about processed texts"""
    return business_logic.get_processing_stats()

@app.get("/recent-activity/{hours}")
async def get_recent_activity(hours: int = 24):
    """Get processing activity from the last N hours"""
    return business_logic.get_recent_activity(hours)

@app.get("/sentiment-distribution")
async def get_sentiment_distribution():
    """Get distribution of sentiment analysis results"""
    return business_logic.get_sentiment_distribution()

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "provider": os.getenv("LLM_PROVIDER", "huggingface")}
