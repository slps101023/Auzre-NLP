from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import configparser
from deep_translator import GoogleTranslator
from . import Entity_Recognition

def analyze_sentiment_and_keywords(text):
    config = configparser.ConfigParser()
    config.read("C:\\Users\\User\\Documents\\NLP\\NLP_Final_Project\\backend\\config.ini")  # 列出所有的 section，確認是否成功讀取
    text_analytics_client = TextAnalyticsClient(
        endpoint=config["AzureTextAnalytics"]["AZURE_LANGUAGE_ENDPOINT"], 
        credential=AzureKeyCredential(config["AzureTextAnalytics"]["AZURE_LANGUAGE_KEY"]),
        default_language="en"
        #default_language="zh-Hant"  #分析中文可能導致找不到wiki資料，如果情緒跟關鍵字需要中文，建議跟wiki拆開
    ) 

    try:
        # 1. 情緒分析
        result_analysis = text_analytics_client.analyze_sentiment(
            [text], 
            show_opinion_mining=True
        )
        sentiment = result_analysis[0].sentiment if not result_analysis[0].is_error else "unknown"
        confidence_scores = result_analysis[0].confidence_scores if not result_analysis[0].is_error else {}
        sentiment_result = {
            "sentiment": sentiment,
            "confidence_scores": {
                "positive": confidence_scores.positive if confidence_scores else 0,
                "neutral": confidence_scores.neutral if confidence_scores else 0,
                "negative": confidence_scores.negative if confidence_scores else 0
            }
        }

        # # wiki link(Azure Text Analytics 的實體連結功能)
        # result_wiki = text_analytics_client.recognize_linked_entities(
        #     [text],
        # )
        # docs_wiki = [doc_wiki for doc_wiki in result_wiki if not doc_wiki.is_error]
        # entity_to_url = []
        # for doc_wiki in docs_wiki:
        #     for entity in doc_wiki.entities:
        #         if entity.data_source == "Wikipedia":
        #             entity_to_url.append({"name": entity.name, "url": entity.url})
        # translator = GoogleTranslator(source='en', target='zh-TW')
        # for item in entity_to_url:
        #     original_name = item['name']
        #     translated_name = translator.translate(original_name)
        #     item['name'] = translated_name  # 直接替換掉原本的 name
        # return sentiment_result, entity_to_url
    
        # wiki link (spacy_entity_linker 的實體連結功能)
        result_wiki = Entity_Recognition.extract_entities(text)
        translator = GoogleTranslator(source='en', target='zh-TW')
        for item in result_wiki:
            original_name = item['name']
            translated_name = translator.translate(original_name)
            item['name'] = translated_name  # 直接替換掉原本的 name
        return sentiment_result, result_wiki
    except KeyError:
        return {"error": "找不到設定檔或內容不完整，請確認 config.ini 的格式是否正確。"}

if __name__ == "__main__":
    sample_text = "Microsoft and OpenAI today announced a new multi-billion dollar investment to build a massive supercomputer across data centers in the United States. The breakthrough project, codenamed 'Stargate,' aims to push the boundaries of artificial intelligence and machine learning. While tech investors are highly optimistic about the potential economic growth and innovation, some environmental commentators have raised serious concerns about the substantial carbon footprint and energy consumption of these new facilities."
    sentiment_result, entity_to_url = analyze_sentiment_and_keywords(sample_text)
    print("Sentiment Analysis Result:")
    print(sentiment_result)
    print("\nRecognized Entities and their Wikipedia URLs:")
    print(entity_to_url)