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
    「Microsoft 與 OpenAI 今日宣布一項數十億美元的新投資，將在美國多個資料中心建造一台大型超級電腦。這項代號為「星際之門」的突破性計畫，旨在推動人工智慧與機器學習的界限。雖然科技投資者對潛在的經濟成長與創新高度樂觀，但部分環保評論人士對這些新設施的龐大碳足跡與能源消耗表示嚴重擔憂。」
    """
    print(summarize_text(sample_text))