from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services import translator, Sentiment, summary, speech, scraper
from services import analyze_news_text, crawl_and_analyze_news
from pydantic import BaseModel
import os
import time

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
    start_time = time.time()
    
    result = await analyze_news_text(news_request.news_text)

    end_time = time.time()
    duration = end_time - start_time

    print(f"⚡ 非同步並發管線總共耗時: {duration:.2f} 秒")

    return result

@app.post("/crawler")
async def crawler(crawler_input: CrawlerInput):
    # 直接呼叫網址爬蟲分析函數
    start_time = time.time()
    
    result = await crawl_and_analyze_news(crawler_input.url)

    end_time = time.time()
    duration = end_time - start_time
    print(f"⚡ 爬蟲 + 分析管線總共耗時: {duration:.2f} 秒")
    
    return result

# @app.post("/analyze")
# async def analyze(news_request: NewsRequest):
#     start_time = time.time()
#     # Placeholder for actual analysis logic
#     translated_text = translator.translate_news_to_zh(news_request.news_text)
#     sentiment_result, entity_to_url = Sentiment.analyze_sentiment_and_keywords(news_request.news_text)
#     summary_result = summary.summarize_text(news_request.news_text)
#     speech_result = speech.azure_speech(summary_result)
#     mockResult = {
#         "original_text": news_request.news_text,
#         "translated_text": translated_text,
#         "sentiment": sentiment_result,
#         "summary": summary_result,
#         "entities": entity_to_url,
#         "audio_url": speech_result
#     };

#     print(f"分析結果: {mockResult}")  # 印出分析結果，確認格式正確

#     end_time = time.time()
#     duration = end_time - start_time
#     print(f" 同步分析管線總共耗時: {duration:.2f} 秒")

#     return mockResult

# @app.post("/crawler")
# async def crawler(crawler_input: CrawlerInput):
#     start_time = time.time()

#     crawled_data = scraper.fetch_news_article(crawler_input.url)
#     translated_text = translator.translate_news_to_zh(crawled_data)
#     sentiment_result, entity_to_url = Sentiment.analyze_sentiment_and_keywords(crawled_data)
#     summary_result = summary.summarize_text(crawled_data)
#     speech_result = speech.azure_speech(summary_result)

#     mockResult = {
#         "original_text": crawled_data,
#         "translated_text": translated_text,
#         "sentiment": sentiment_result,
#         "summary": summary_result,
#         "entities": entity_to_url,
#         "audio_url": speech_result
#     };
#     end_time = time.time()
#     duration = end_time - start_time
#     print(f" 同步爬蟲 + 分析管線總共耗時: {duration:.2f} 秒")

#     return mockResult
#  啟動 python -m uvicorn main:app --reload