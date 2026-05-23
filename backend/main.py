from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services import translator
from pydantic import BaseModel
from services import Sentiment
from services import summary
from services import speech
import os

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允許前端的網址
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法（包含 POST, OPTIONS, GET 等）
    allow_headers=["*"],  # 允許所有 Header
)

class NewsRequest(BaseModel):
    news_text: str

@app.get("/")
async def root():
    return {"message": "Server is running!"}

@app.post("/analyze")
async def analyze(news_request: NewsRequest):
    # Placeholder for actual analysis logic
    translated_text = translator.translate_news_to_zh(news_request.news_text)
    sentiment_result, entity_to_url = Sentiment.analyze_sentiment_and_keywords(news_request.news_text)
    summary_result = summary.summarize_text(news_request.news_text)
    speech_result = "http://localhost:8000/static/audio/chinese_audio.mp3"
    mockResult = {
        "original_text": news_request.news_text,
        "translated_text": translated_text,
        "sentiment": sentiment_result,
        "summary": summary_result,
        "entities": entity_to_url,
        "audio_url": speech_result
    };
    print(mockResult)
    return mockResult

@app.post("/crawler")
async def crawler(url: str):
    # Placeholder for actual crawling logic
    return {"crawled_data": f"Crawled data from: {url}"}