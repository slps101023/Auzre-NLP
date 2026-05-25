from .translator import translator
from .Sentiment import Sentiment
from .summary import summary
from .speech import speech
from .scraper import scraper

def analyze_news_text(news_text: str) -> dict:
    """
    函數一：負責純文字新聞的完整分析管線
    """
    translated_text = translator.translate_news_to_zh(news_text)
    sentiment_result, entity_to_url = Sentiment.analyze_sentiment_and_keywords(news_text)
    summary_result = summary.summarize_text(news_text)
    speech_result = speech.azure_speech(summary_result)
    
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


def crawl_and_analyze_news(url: str) -> dict:
    """
    函數二：負責爬取網址，並直接複用文字分析管線
    """
    crawled_data = scraper.fetch_news_article(url)
    
    # 爬下來的文本直接丟給上面的函數處理，邏輯完全一致，還能少寫一次重複的程式碼！
    return analyze_news_text(crawled_data)