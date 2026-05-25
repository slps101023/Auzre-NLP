from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services import analyze_news_text, crawl_and_analyze_news
from pydantic import BaseModel
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

class CrawlerInput(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "Server is running!"}

@app.post("/analyze")
async def analyze(news_request: NewsRequest):
    # 直接呼叫純文字分析函數
    return analyze_news_text(news_request.news_text)

@app.post("/crawler")
async def crawler(crawler_input: CrawlerInput):
    # 直接呼叫網址爬蟲分析函數
    return crawl_and_analyze_news(crawler_input.url)

#  啟動 python -m uvicorn main:app --reload