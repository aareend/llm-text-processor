
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class InMemoryStorage:
    def __init__(self):
        self.results: Dict[str, dict] = {}
    
    def save_result(self, original_text: str, processed_result: dict, task_type: str) -> dict:
        """Save a processed result to storage and return the complete record"""
        result_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        result = {
            "id": result_id,
            "original_text": original_text,
            "processed_result": processed_result,
            "task_type": task_type,
            "created_at": timestamp
        }
        
        self.results[result_id] = result
        return result
    
    def get_all_results(self) -> List[dict]:
        """Retrieve all processed results"""
        return list(self.results.values())
    
    def get_result_by_id(self, result_id: str) -> Optional[dict]:
        """Retrieve a specific result by ID"""
        return self.results.get(result_id)

# Create a singleton instance
storage = InMemoryStorage()
