from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from newsapi import NewsApiClient
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

# Load environment variables from .env file

load_dotenv(override=True)


# Initialize FastAPI app
app = FastAPI()

# Load Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize NewsAPI client (replace with your NewsAPI key)
# Fetch API key from environment variables
news_api_key = os.getenv("NEWS_API_KEY")

if not news_api_key:
    raise ValueError("NEWS_API_KEY not found. Make sure it is set in the .env file.")

# Initialize NewsAPI client
newsapi = NewsApiClient(api_key=news_api_key)

# Load Sentiment Analysis model (Hugging Face)
sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
sentiment_classifier = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)


# Pydantic model for request
class SummarizeRequest(BaseModel):
    keyword: str
    language: str = "en"
    num_articles: int = 5


class KeywordRequest(BaseModel):
    keyword: str
    language: str = "en"
    num_articles: int = 5


class SentimentRequest(BaseModel):
    text: str


# Helper function: Fetch news articles using NewsAPI
def fetch_news_articles(keyword, language, num_articles):
    try:
        # Fetch the top headlines for the given keyword and language
        response = newsapi.get_everything(
            q=keyword,
            language=language,
            page_size=num_articles,
            sort_by="relevancy"
        )
        return response['articles']
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching news articles: " + str(e))


# Endpoint for summarizing articles
@app.post("/summarize")
async def summarize_article(request: SummarizeRequest):
    try:
        # Fetch the latest news articles
        articles = fetch_news_articles(request.keyword, request.language, request.num_articles)

        # Summarize each article
        summaries = []
        for article in articles:
            text = article['content']  # Assuming the content is the article body
            if text:
                # Summarize with Hugging Face model
                summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
                summarized_text = summary[0]['summary_text']

                # Append results
                summaries.append({
                    "title": article['title'],
                    "summary": summarized_text,
                    "source": article['source']['name'],
                    "url": article['url']
                })

        return {"keyword": request.keyword, "language": request.language, "results": summaries}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint for fetching articles by keyword (without summarizing)
@app.post("/fetch_articles")
async def fetch_articles(request: KeywordRequest):
    try:
        # Fetch articles based on keyword
        articles = fetch_news_articles(request.keyword, request.language, request.num_articles)

        # Return raw articles
        return {"keyword": request.keyword, "language": request.language, "articles": articles}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint for sentiment analysis of a given text
@app.post("/analyze_sentiment")
async def analyze_sentiment(request: SentimentRequest):
    try:
        # Analyze sentiment of the given text
        sentiment_result = sentiment_classifier(request.text)

        return {"text": request.text, "sentiment": sentiment_result[0]["label"],
                "confidence": sentiment_result[0]["score"]}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
