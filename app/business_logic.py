# app/business_logic.py
from datetime import datetime, timedelta
from typing import List, Dict, Any

class BusinessLogic:
    def __init__(self, storage):
        self.storage = storage
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Calculate statistics about processed texts"""
        results = self.storage.get_all_results()
        
        # Count by task type
        task_counts = {}
        for result in results:
            task = result["task_type"]
            if task not in task_counts:
                task_counts[task] = 0
            task_counts[task] += 1
        
        # Calculate average text length
        if results:
            avg_text_length = sum(len(r["original_text"]) for r in results) / len(results)
        else:
            avg_text_length = 0
            
        return {
            "total_processed": len(results),
            "by_task_type": task_counts,
            "average_text_length": round(avg_text_length, 2)
        }
    
    def get_recent_activity(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get processing activity from the last N hours"""
        results = self.storage.get_all_results()
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_results = [
            r for r in results 
            if isinstance(r["created_at"], datetime) and r["created_at"] > cutoff_time
        ]
        
        return recent_results
    
    def get_sentiment_distribution(self) -> Dict[str, int]:
        """Get distribution of sentiment analysis results"""
        results = self.storage.get_all_results()
        sentiment_results = [
            r for r in results 
            if r["task_type"] == "sentiment"
        ]
        
        distribution = {}
        for result in sentiment_results:
            sentiment = result["processed_result"].get("sentiment", "UNKNOWN")
            if sentiment not in distribution:
                distribution[sentiment] = 0
            distribution[sentiment] += 1
            
        return distribution
