# Text Summarization and NLP API

This is a FastAPI-based web application that provides various Natural Language Processing (NLP) functionalities, including text summarization, sentiment analysis, content generation, news fetching, and translation. The API leverages powerful models from Hugging Face and external news services like NewsAPI to deliver real-time processing and insights on textual data.

### Features
- **Text Summarization**: Summarizes long texts into concise versions using the `facebook/bart-large-cnn` model.
- **Sentiment Analysis**: Analyzes the sentiment (positive/negative/neutral) of a given text.
- **Content Generation**: Generates text based on user-defined prompts using the `GPT-2` model.
- **News Fetching**: Fetches the latest news articles based on a specified keyword, with filtering options (like language and date range) via the NewsAPI service.
- **Language Translation**: Translates text from one language to another using Hugging Face translation models (e.g., English to Spanish).
- **Sentiment Analysis on Summarized Text**: A combined endpoint that first summarizes the provided text and then performs sentiment analysis on the summary.

### Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/nlp-api.git
    cd nlp-api
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    - `NEWS_API_KEY`: You will need a NewsAPI key to fetch news articles. You can get it by signing up [here](https://newsapi.org/).
    
4. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

5. Open your browser and go to `http://127.0.0.1:8000/docs` to interact with the API via the Swagger UI.

### Endpoints

- `/summarize`: Summarizes a given text.
- `/analyze_sentiment`: Analyzes the sentiment of a provided text.
- `/generate_content`: Generates text based on a user prompt.
- `/fetch_news`: Fetches news articles based on a keyword.
- `/translate_text`: Translates a given text into a specified target language.
- `/summarize_and_analyze`: Summarizes a text and analyzes the sentiment of the summary.

### Technologies Used
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **Hugging Face Transformers**: Pre-trained transformer models for various NLP tasks like summarization, sentiment analysis, content generation, and more.
- **NewsAPI**: A simple HTTP REST API for accessing news articles from multiple sources.

### License
This project is licensed under the MIT License.
