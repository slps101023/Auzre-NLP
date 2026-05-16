import configparser
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

def translate_news_to_zh(english_text):
    config = configparser.ConfigParser()
    config.read("C:\\Users\\User\\Documents\\NLP\\NLP_Final_Project\\backend\\config.ini")
    print(config.sections())  # 列出所有的 section，確認是否成功讀取

    try:
        # 2. 建立 Azure Translator 的連線客戶端
        text_translator = TextTranslationClient(
            credential=AzureKeyCredential(config["AzureTranslator"]["Key"]),
            endpoint=config["AzureTranslator"]["Endpoint"],
            region=config["AzureTranslator"]["Region"],
        )
    except KeyError:
        return "【錯誤】找不到設定檔或內容不完整，請確認 config.ini 的格式是否正確。"

    # 3. 準備翻譯參數與「分段處理」
    try:
        target_languages = ["zh-Hant"]
        
        # 將長篇新聞依照「換行符號 (\n)」切成多段
        # 同時過濾掉空白的行，保留真正有文字的段落
        paragraphs = [p for p in english_text.split('\n') if p.strip() != ""]
        
        # 如果文章完全是空的，提早結束
        if not paragraphs:
            return "無內容可翻譯"

        # 將切好的段落陣列直接作為 body 送給 API 翻譯
        response = text_translator.translate(
            body=paragraphs, 
            to_language=target_languages
        )
        
        # 4. 解析結果並重新組合段落
        translated_paragraphs = []
        for translation in response:
            if translation and translation.translations:
                # 把每一段的中文翻譯結果抓出來存入陣列
                translated_paragraphs.append(translation.translations[0].text)
        
        # 利用 "\n\n" 將所有翻譯好的段落重新接起來，讓輸出的文章有漂亮的段落間距
        return "\n\n".join(translated_paragraphs)

    # 處理 API 連線或金鑰認證錯誤
    except HttpResponseError as exception:
        return f"【發生錯誤，無法翻譯】: {exception.error.message}"

if __name__ == "__main__":
    print("請貼上你要翻譯的英文新聞全文（支援多段落）。")
    print("【輸入完畢後，請在新的一行輸入 END 並按 Enter 來開始翻譯】：")
    
    lines = []
    while True:
        line = input()
        # 當使用者輸入 END (不分大小寫) 時，才跳出迴圈
        if line.strip().upper() == "END":
            break
        lines.append(line)
        
    user_input_news = "\n".join(lines)
    
    if user_input_news.strip():
        chinese_summary = translate_news_to_zh(user_input_news)
        
        print("\n【中文翻譯】\n")
        print(chinese_summary)
    else:
        print("\n你沒有輸入任何文章！")