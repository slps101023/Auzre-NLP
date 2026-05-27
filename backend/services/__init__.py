from . import translator
from . import Sentiment
from . import summary
from . import speech
from . import scraper
import asyncio

async def analyze_news_text(news_text: str) -> dict:
    """
    函數一：負責純文字新聞的完整分析管線
    """
    task_translate = asyncio.to_thread(translator.translate_news_to_zh, news_text)
    task_sentiment = asyncio.to_thread(Sentiment.analyze_sentiment_and_keywords, news_text)
    task_summary = asyncio.to_thread(summary.summarize_text, news_text)

    # 等待所有非同步任務完成
    translated_text, (sentiment_result, entity_to_url), summary_result = await asyncio.gather(
        task_translate,
        task_sentiment,
        task_summary
    )

    speech_result = await asyncio.to_thread(speech.azure_speech, summary_result)
    
    result = {
        "original_text": news_text,
        "translated_text": translated_text,
        "sentiment": sentiment_result,
        "summary": summary_result,
        "entities": entity_to_url,
        "audio_url": speech_result
    }
    
    print(f"分析結果: {result}")  # 保留你原本的確認日誌
    return result


async def crawl_and_analyze_news(url: str) -> dict:
    """
    函數二：負責爬取網址，並直接複用文字分析管線
    """
    crawled_data = await asyncio.to_thread(scraper.fetch_news_article, url)
    
    # 爬下來的文本直接丟給上面的函數處理，邏輯完全一致，還能少寫一次重複的程式碼！
    return await analyze_news_text(crawled_data)