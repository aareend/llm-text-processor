from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to be processed")

class ProcessedResult(BaseModel):
    id: str
    original_text: str
    processed_result: Dict[str, Any]
    task_type: str
    created_at: datetime

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
