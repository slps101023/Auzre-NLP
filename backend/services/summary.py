import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import configparser
from deep_translator import GoogleTranslator

def summarize_text(text):
    try:
        config = configparser.ConfigParser()
        config.read('C:\\Users\\User\\Documents\\NLP\\NLP_Final_Project\\backend\\config.ini')
        endpoint = config['AzureTextAnalytics']['AZURE_LANGUAGE_ENDPOINT']
        key = config['AzureTextAnalytics']['AZURE_LANGUAGE_KEY']
    except KeyError as e:
        print(f"配置文件中缺少必要的鍵: {e}")
        return  

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )

    documents = [text]

    print("開始提取文章精華...\n" + "-"*40)

    poller = text_analytics_client.begin_extract_summary(
        documents,
        language="zh",
        max_sentence_count=3 
    )

    extract_summary_results = poller.result()

    for idx, result in enumerate(extract_summary_results):
        if result.is_error:
            print(f"文件 {idx} 發生錯誤: 代碼 '{result.error.code}', 訊息 '{result.error.message}'")
        else:
            
            summary_sentences = [sentence.text for sentence in result.sentences]
            final_summary = " ".join(summary_sentences)
            translator = GoogleTranslator(source='en', target='zh-TW')
            final_summary = translator.translate(final_summary)
            return final_summary
                

if __name__ == "__main__":
    sample_text = """
    世界棒球經典賽（WBC）台灣隊傳來捷報，在今天與捷克的對決中，以14比0的分數，7局扣倒捷克，奪下首勝，讓台灣球迷瘋狂歡呼。
    這場比賽台灣隊伍展現了極佳的打擊火力與投手壓制力。先發投手表現亮眼，主投五局僅被擊出零星安打，沒有失分。
    打線方面，第三局一波猛烈攻勢灌進六分奠定勝基。總教練在賽後記者會表示，球員們頂住了壓力，將平時訓練的成果完美發揮。
    接下來台灣隊將迎戰實力強勁的日本隊，這將是晉級複賽的關鍵戰役，全隊將全力以赴準備。
    """
    summarize_text(sample_text)