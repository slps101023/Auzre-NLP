import trafilatura
from fastapi import HTTPException

def fetch_news_article(url: str) -> str:
    """
    接收新聞網址，爬取並回傳乾淨的英文新聞內文
    """
    try:
        # 1. 下載網頁 HTML
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            raise HTTPException(status_code=400, detail="無法下載該網址內容，請檢查網址是否正確。")
        
        # 2. 提取網頁中的「主體新聞文章」（自動過濾廣告、側邊欄、頁尾導覽）
        # include_comments=False: 不抓取網友留言
        # no_fallback=False: 如果主要演算法失敗，使用備用方案確保抓到文字
        article_text = trafilatura.extract(downloaded, include_comments=False, no_fallback=False)
        
        if not article_text or len(article_text.strip()) < 50:
            raise HTTPException(status_code=400, detail="無法從該網頁提取足夠的新聞內文，可能是防爬蟲網站。")
            
        return article_text
        
    except Exception as e:
        print(f"爬取新聞失敗: {e}")
        raise HTTPException(status_code=500, detail=f"新聞爬取失敗: {str(e)}")

# 測試用區塊：你可以直接執行 python services/scraper.py 測試
if __name__ == "__main__":
    test_url = "https://edition.cnn.com/2026/05/22/us/chemical-spill-orange-county-california" # 範例網址
    try:
        print("正在測試爬取 CNN 新聞...")
        text = fetch_news_article(test_url)
        print("\n--- 成功抓取前 300 個字 ---")
        print(text)
    except Exception as e:
        print(e)