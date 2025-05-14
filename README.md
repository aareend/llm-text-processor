# LLM Text Processor API

A RESTful API for processing text using Large Language Models (LLMs) with text summarization, named entity recognition, and sentiment analysis capabilities.

## Features

- **Text Processing**: Process text using state-of-the-art language models
- **Multiple Tasks**: Support for text summarization, named entity extraction, and sentiment analysis
- **Flexible LLM Providers**: Switch between OpenAI and Hugging Face models
- **Request History**: In-memory storage of processed requests
- **Analytics**: Statistics on processed texts, sentiment distribution, and recent activity
- **RESTful API**: Clean API design with FastAPI

## Project Structure

```
llm-text-processor/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # Data models
│   ├── llm_service.py       # LLM integration
│   ├── storage.py           # In-memory storage
│   └── business_logic.py    # Additional business logic
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
├── run.py                   # Run script
└── README.md                # Documentation
```

## Requirements

- Python 3.8+
- FastAPI
- OpenAI API key (if using OpenAI)
- Hugging Face Transformers (if using local models)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/llm-text-processor.git
   cd llm-text-processor
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   
   Create a `.env` file in the project root with the following variables:
   ```
   # For OpenAI:
   OPENAI_API_KEY=your_openai_api_key_here
   LLM_PROVIDER=openai
   
   # OR for Hugging Face (no API key required for most models):
   # LLM_PROVIDER=huggingface
   ```

## Running the Application

Start the FastAPI server:

```bash
python run.py
```

The API will be available at http://localhost:8000

You can access the Swagger UI documentation at http://localhost:8000/docs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with API information |
| `/process` | POST | Process text with LLM |
| `/history` | GET | Get processing history |
| `/stats` | GET | Get processing statistics |
| `/recent-activity/{hours}` | GET | Get recent activity |
| `/sentiment-distribution` | GET | Get sentiment distribution |
| `/health` | GET | Health check |

### Detailed Endpoint Descriptions

#### `POST /process`

Process text with an LLM.

**Query Parameters:**
- `task` (optional): The processing task to perform. Options: `summarize`, `entities`, `sentiment`. Default: `summarize`.

**Request Body:**
```json
{
  "text": "Text to be processed"
}
```

**Example Response:**
```json
{
  "id": "4f7d6e8a-1b2c-4d3e-8f9a-0b1c2d3e4f5a",
  "original_text": "Text to be processed",
  "processed_result": {
    "summary": "Summarized text"
    // The structure varies based on the task
  },
  "task_type": "summarize",
  "created_at": "2023-11-14T12:34:56.789123"
}
```

#### `GET /history`

Retrieve all processed text results.

**Example Response:**
```json
[
  {
    "id": "4f7d6e8a-1b2c-4d3e-8f9a-0b1c2d3e4f5a",
    "original_text": "Text to be processed",
    "processed_result": { ... },
    "task_type": "summarize",
    "created_at": "2023-11-14T12:34:56.789123"
  },
  ...
]
```

#### `GET /stats`

Get statistics about processed texts.

**Example Response:**
```json
{
  "total_processed": 3,
  "by_task_type": {
    "summarize": 1,
    "entities": 1,
    "sentiment": 1
  },
  "average_text_length": 120.33
}
```

#### `GET /recent-activity/{hours}`

Get processing activity from the last N hours.

**Path Parameters:**
- `hours` (optional): Number of hours to look back. Default: 24.

**Example Response:**
```json
[
  {
    "id": "4f7d6e8a-1b2c-4d3e-8f9a-0b1c2d3e4f5a",
    "original_text": "Text to be processed",
    "processed_result": { ... },
    "task_type": "summarize",
    "created_at": "2023-11-14T12:34:56.789123"
  },
  ...
]
```

#### `GET /sentiment-distribution`

Get distribution of sentiment analysis results.

**Example Response:**
```json
{
  "POSITIVE": 2,
  "NEGATIVE": 1,
  "NEUTRAL": 0
}
```

#### `GET /health`

Check if the API is running.

**Example Response:**
```json
{
  "status": "healthy",
  "provider": "openai"
}
```

## Example Usage

### Using cURL

#### Process Text (Summarization):

```bash
curl -X POST "http://localhost:8000/process?task=summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals."}'
```

#### Process Text (Named Entity Recognition):

```bash
curl -X POST "http://localhost:8000/process?task=entities" \
     -H "Content-Type: application/json" \
     -d '{"text": "Apple Inc. is planning to open a new store in New York City, according to CEO Tim Cook."}'
```

#### Process Text (Sentiment Analysis):

```bash
curl -X POST "http://localhost:8000/process?task=sentiment" \
     -H "Content-Type: application/json" \
     -d '{"text": "I really enjoyed the movie. It was fantastic!"}'
```

### Using Python

```python
import requests
import json

# Base URL
base_url = "http://localhost:8000"

# Test summarization
response = requests.post(
    f"{base_url}/process", 
    params={"task": "summarize"},
    json={"text": "This is a test text that needs to be summarized. It contains several sentences about various topics."}
)
print(json.dumps(response.json(), indent=2))

# Get history
response = requests.get(f"{base_url}/history")
print(json.dumps(response.json(), indent=2))
```

## Changing LLM Provider

The application supports two LLM providers:

1. **OpenAI** (requires API key)
2. **Hugging Face** (free local models)

To change the provider, edit the `.env` file:

```
# For OpenAI:
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai

# OR for Hugging Face:
LLM_PROVIDER=huggingface
```

## Troubleshooting

### Common Issues

1. **API Key Issues**: 
   - Ensure your OpenAI API key is correct in the `.env` file
   - Check that you have sufficient credits in your OpenAI account

2. **Model Loading Issues**: 
   - When using Hugging Face for the first time, models will be downloaded
   - This may take some time and requires a good internet connection
   - Ensure you have enough disk space for the models (several GB)

3. **Memory Issues**:
   - Hugging Face models can use significant memory
   - If you're on a low-memory system, consider using the OpenAI provider

### Checking Logs

The application logs information to the console. Check the logs for any error messages if you're having issues.

## Limitations

1. **In-Memory Storage**: All data is stored in memory and is lost when the application restarts. In a production environment, you would want to use a persistent database.

2. **No Authentication**: This implementation doesn't include authentication. For production use, add proper authentication and authorization.

3. **Rate Limiting**: When using OpenAI, be aware of API rate limits and costs.

## Future Enhancements

Potential improvements for this project:

1. Add persistent storage (database integration)
2. Implement user authentication
3. Add more LLM tasks (translation, question answering, etc.)
4. Implement caching for repeated requests
5. Add batch processing capabilities

## License

[MIT](LICENSE)
