from keybert import KeyBERT

# 1. 初始化模型 (英文專用模型)
kw_model = KeyBERT(model='all-MiniLM-L6-v2')

def filter_top_10_entities(article_text: str, recognized_entities: list) -> list:
    """
    輸入文章與原始實體列表，依據 URL 進行去重，並回傳依相關性排序的前 5 名實體
    """
    
    # 🎯 核心修正：用 URL 當作字典的 Key 來達到「URL 去重」！
    # 如果有重複的 URL（例如 whale 和 whales），後面的會覆蓋前面的，確保一個 URL 只會留下一個名字。
    unique_entities_by_url = {}
    for item in recognized_entities:
        url = item['url']
        # 這裡可以做個小優化：如果 URL 已經存在，可以優先保留比較長的字（通常比較完整，比如優先留 blue whales 捨棄 whales）
        if url in unique_entities_by_url:
            existing_name = unique_entities_by_url[url]
            if len(item['name']) > len(existing_name):
                unique_entities_by_url[url] = item['name']
        else:
            unique_entities_by_url[url] = item['name']

    # 1. 現在我們有一組「URL 絕對不重複」的乾淨實體了
    # 抽出準備餵給 KeyBERT 的候選詞，並統一轉小寫（避免 sklearn 噴警告）
    candidate_words = list(set([name.lower() for name in unique_entities_by_url.values()]))
    
    if not candidate_words:
        return []
    
    # 2. 讓 KeyBERT 進行語意相關性評分
    keywords_with_scores = kw_model.extract_keywords(
        article_text,
        candidates=candidate_words, 
        stop_words='english',
        top_n=5  # 🎯 順應你的程式碼改成前 5 名                  
    )
    
    # 3. 建立反向查詢字典（因為 KeyBERT 回傳的是小寫 name，我們要拿小寫 name 去查原本的大寫 name 與 URL）
    # 注意：因為前面已經用 URL 去重過了，這裡直接建立 mapping 不會有多餘的重複
    name_mapping = {}
    url_mapping = {}
    for url, original_name in unique_entities_by_url.items():
        lowered_name = original_name.lower()
        name_mapping[lowered_name] = original_name
        url_mapping[lowered_name] = url
    
    # 4. 組合最終結果
    top_5_results = []
    for word, score in keywords_with_scores:
        top_5_results.append({
            "name": name_mapping.get(word, word),          # 還原原本漂亮的大寫
            "url": url_mapping.get(word, "URL not found"), # 拿到對應的唯一的 URL
            "relevance_score": round(float(score), 4)
        })
        
    return top_5_results

# ================= 測試執行 =================
if __name__ == "__main__":
    sample_text = 'Scientists are using Artificial Intelligence (AI) to save endangered whales in the ocean.\n\nAn organization called "Ocean Voice" has placed underwater microphones in the Pacific Ocean. These microphones record thousands of hours of ocean sounds. Because humans cannot listen to all the recordings, scientists trained an AI program to help.\n\nThe AI can recognize the unique songs of different whale species, such as blue whales and humpback whales. When the AI hears a whale near a busy shipping lane, it sends an automatic warning to nearby ships. The captains can then slow down their vessels to avoid hitting the animals.\n\n"This technology is a game-changer," said Dr. Sarah Lin, a marine biologist. "It allows us to protect whales in real-time and keep the oceans safe."'
    
    sample_entity = [
        {'name': 'Scientists', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q898207'}, 
        {'name': 'Artificial Intelligence', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q221113'}, 
        {'name': 'AI', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q11660'}, 
        {'name': 'whales', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q1865281'}, 
        {'name': 'ocean', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q9430'}, 
        {'name': 'organization', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q43229'}, 
        {'name': 'Voice', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q27949148'}, 
        {'name': 'microphones', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q46384'}, 
        {'name': 'Pacific Ocean', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q98'}, 
        {'name': 'thousands', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q43016'}, 
        {'name': 'hours', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q25235'}, 
        {'name': 'humans', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q5'}, 
        {'name': 'recordings', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q7302910'}, 
        {'name': 'scientists', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q901'}, 
        {'name': 'songs', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q7366'}, 
        {'name': 'species', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q7432'}, 
        {'name': 'blue whales', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q42196'}, 
        {'name': 'humpback whales', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q132905'}, 
        {'name': 'whale', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q1865281'}, 
        {'name': 'shipping lane', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q1757209'}, 
        {'name': 'warning', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q7969813'}, 
        {'name': 'ships', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q11446'}, 
        {'name': 'captains', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q19100'}, 
        {'name': 'vessels', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q11446'}, 
        {'name': 'animals', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q729'}, 
        {'name': 'technology', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q11016'}, 
        {'name': 'game', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q11410'}, 
        {'name': 'Dr.', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q4618975'}, 
        {'name': 'biologist', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q864503'}, 
        {'name': 'time', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q11471'}, 
        {'name': 'oceans', 'url': 'https://www.wikidata.org/wiki/Special:GoToLinkedPage/enwiki/Q9430'}
    ]
    
    import pprint
    pprint.pprint(filter_top_10_entities(sample_text, sample_entity))