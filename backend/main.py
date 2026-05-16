from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import translator
from pydantic import BaseModel

app = FastAPI()

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
    return {"message": "Hello World!"}

@app.post("/analyze")
async def analyze(news_request: NewsRequest):
    # Placeholder for actual analysis logic
    translated_text = translator.translate_news_to_zh(news_request.news_text)
    mockResult = {
        "original_text": news_request.news_text,
        "translated_text": translated_text,
        "sentiment": {
            "sentiment": "mixed",
            "confidence_scores": {
                "positive": 0.45,
                "neutral": 0.10,
                "negative": 0.45
            }
        },
        "summary": "微軟與 OpenAI 宣布斥資數十億美元在美國建設名為「星門」的 AI 超級電腦，此舉雖受投資者看好，但也引發了環保人士對能源消耗的擔憂。",
        "entities": [
            { "name": "微軟", "url": "https://zh.wikipedia.org/wiki/微軟" },
            { "name": "OpenAI", "url": "https://zh.wikipedia.org/wiki/OpenAI" },
            { "name": "人工智慧", "url": "https://zh.wikipedia.org/wiki/人工智慧" },
            { "name": "機器學習", "url": "https://zh.wikipedia.org/wiki/機器學習" }
        ],
        "audio_url": "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars3.wav"
    };
    return mockResult

@app.post("/crawler")
async def crawler(url: str):
    # Placeholder for actual crawling logic
    return {"crawled_data": f"Crawled data from: {url}"}