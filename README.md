# Evolusis – AI Reasoning Agent

Evolusis is an AI-powered reasoning agent built with FastAPI. It leverages Google's Gemini LLM for natural language processing, integrates with NewsAPI for real-time news retrieval, and maintains short-term memory for conversational context. The agent detects user intents (e.g., news queries vs. general questions) and responds accordingly with concise, factual answers.

## Features

- **Intent Detection**: Automatically identifies news-related queries and fetches relevant articles.
- **News Integration**: Uses NewsAPI to retrieve and summarize recent news articles based on topics.
- **LLM Responses**: Generates helpful answers using Google's Gemini model, avoiding hallucinations by citing provided data.
- **Short-Term Memory**: Retains the last 5 query-answer pairs for contextual responses.
- **FastAPI Backend**: Provides a RESTful API for easy integration and deployment.
- **Logging**: Comprehensive logging with Loguru for debugging and monitoring.

## Installation

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-2.5-flash  # Optional, defaults to gemini-2.5-flash
   NEWS_API_KEY=your_newsapi_key_here
   ```
   - Obtain a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).
   - Obtain a NewsAPI key from [NewsAPI](https://newsapi.org/).

## Usage

1. Run the FastAPI server:

   ```
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://127.0.0.1:8000`.

3. Access the interactive API documentation at `http://127.0.0.1:8000/docs`.

### API Endpoints

- **GET /**: Health check endpoint.

  - Response: `{"status": "ok", "message": "Agent is running."}`

- **POST /ask**: Submit a query to the agent.
  - Request Body:
    ```json
    {
      "query": "What is the weather in Paris today?"
    }
    ```
  - Response:
    ```json
    {
      "reasoning": "Detected intent: news\nFetched recent articles using NewsAPI.",
      "answer": "The provided articles do not contain information about the weather in Paris today. They cover topics related to climate and energy news roundups, an opinion piece on climate change, a general news summary, and a UN press briefing, all from late October and early November 2025."
    }
    ```

### Example Queries

- General question: `"What is the capital of France?"`
- News query: `"Latest news on AI"`

## Project Structure

- `app/agent.py`: Core agent logic, orchestrates intent detection, LLM calls, and tool usage.
- `app/intents.py`: Detects user intents (news vs. general) and extracts topics.
- `app/llm_gemini.py`: Wrapper for interacting with Google's Gemini LLM.
- `app/news_service.py`: Handles news fetching and formatting from NewsAPI.
- `app/memory.py`: Manages short-term conversational memory.
- `app/models.py`: Pydantic models for API requests and responses.
- `app/settings.py`: Configuration management using environment variables.
- `app/main.py`: FastAPI application setup and endpoints.

## Dependencies

- fastapi: Web framework for building APIs.
- uvicorn: ASGI server for running FastAPI.
- httpx: Asynchronous HTTP client for API calls.
- pydantic: Data validation and serialization.
- python-dotenv: Environment variable loading.
- loguru: Logging library.
- google-generativeai: Google's Gemini SDK (install separately if needed: `pip install google-generativeai`).

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test thoroughly.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
