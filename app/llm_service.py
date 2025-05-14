
import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get provider from environment
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface")

class LLMService:
    def __init__(self):
        self.provider = LLM_PROVIDER.lower()
        logger.info(f"Initializing LLM service with provider: {self.provider}")
        
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "huggingface":
            self._init_huggingface()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            import openai
            
            # Get API key from environment
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
            
            # Initialize client
            self.client = openai.OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
            
        except ImportError:
            raise ImportError("OpenAI package not installed. Install it with: pip install openai")
    
    def _init_huggingface(self):
        """Initialize Hugging Face pipelines"""
        try:
            from transformers import pipeline
            
            # Optional: Use Hugging Face API token for gated models
            hf_token = os.getenv("HF_API_TOKEN")
            
            # Initialize pipelines with smaller, more efficient models
            logger.info("Loading Hugging Face models (this may take a moment)...")
            
            # Use smaller models for faster loading and less memory usage
            self.summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                token=hf_token
            )
            
            self.ner_pipeline = pipeline(
                "ner", 
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                token=hf_token
            )
            
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                token=hf_token
            )
            
            logger.info("Hugging Face models loaded successfully")
            
        except ImportError:
            raise ImportError("Transformers package not installed. Install it with: pip install transformers torch")
    
    def summarize_text(self, text: str) -> Dict[str, Any]:
        """Summarize the input text"""
        # Check if text is too short for summarization
        if len(text.split()) < 30:
            return {"summary": text, "note": "Text too short for meaningful summarization"}
        
        if self.provider == "openai":
            # Use OpenAI for summarization
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                    {"role": "user", "content": f"Please summarize the following text in a concise paragraph:\n\n{text}"}
                ],
                max_tokens=150
            )
            return {"summary": response.choices[0].message.content.strip()}
            
        else:  # Hugging Face
            # Process with Hugging Face model
            summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            return {"summary": summary[0]['summary_text']}
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities from the input text"""
        if self.provider == "openai":
            # Use OpenAI for entity extraction
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Extract named entities from the text and categorize them by type (PERSON, ORGANIZATION, LOCATION, etc.). Return the result as a JSON object."},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the JSON response
            import json
            try:
                result = json.loads(response.choices[0].message.content)
                return {"entities": result}
            except json.JSONDecodeError:
                return {"entities": {}, "error": "Failed to parse entity extraction result"}
                
        else:  # Hugging Face
            entities = self.ner_pipeline(text)
            
            # Group entities by type
            grouped_entities = {}
            for entity in entities:
                entity_type = entity['entity']
                if entity_type not in grouped_entities:
                    grouped_entities[entity_type] = []
                
                grouped_entities[entity_type].append({
                    "word": entity['word'],
                    "score": round(entity['score'], 3)
                })
                
            return {"entities": grouped_entities}
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze the sentiment of the input text"""
        if self.provider == "openai":
            # Use OpenAI for sentiment analysis
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Analyze the sentiment of the text and return only a JSON object with 'sentiment' (POSITIVE, NEGATIVE, or NEUTRAL) and 'score' (a number between 0 and 1 indicating confidence)."},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the JSON response
            import json
            try:
                result = json.loads(response.choices[0].message.content)
                return result
            except json.JSONDecodeError:
                return {"sentiment": "NEUTRAL", "score": 0.5, "error": "Failed to parse sentiment analysis result"}
                
        else:  # Hugging Face
            sentiment = self.sentiment_analyzer(text)[0]
            return {
                "sentiment": sentiment['label'],
                "score": round(sentiment['score'], 3)
            }
    
    def process_text(self, text: str, task: str = "summarize") -> Dict[str, Any]:
        """Process text based on the specified task"""
        logger.info(f"Processing text with task: {task} using {self.provider}")
        
        if task == "summarize":
            return self.summarize_text(text)
        elif task == "entities":
            return self.extract_entities(text)
        elif task == "sentiment":
            return self.analyze_sentiment(text)
        else:
            raise ValueError(f"Unsupported task: {task}")

# Create a singleton instance
llm_service = LLMService()
