import os
import configparser
import azure.cognitiveservices.speech as speechsdk

# 初始化 Config Parser 讀取金鑰
config = configparser.ConfigParser()
config.read('C:\\Users\\User\\Documents\\NLP\\NLP_Final_Project\\backend\\config.ini')

# 初始化 Azure Speech 設定
speech_config = speechsdk.SpeechConfig(
    subscription=config['AzureSpeech']['SPEECH_KEY'],
    region=config['AzureSpeech']['SPEECH_REGION']
)

def azure_speech(user_input):
    # 設定音訊輸出格式為 MP3
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3
    )
    # 設定為台灣繁體中文女性自然語音模型
    speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"
    
    file_name = "chinese_audio.mp3"
    file_path = os.path.join("C:\\Users\\User\\Documents\\NLP\\NLP_Final_Project\\backend\\static\\audio", file_name)
    
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config
    )

    # 執行非同步語音合成
    result = speech_synthesizer.speak_text_async(user_input).get()
    
    # 檢查合成結果
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"✅ 語音合成成功：[{user_input}]，已儲存至 [{file_path}]")
        return file_path
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"❌ 語音合成取消: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"錯誤詳細資訊: {cancellation_details.error_details}")
        return "ERROR"

if __name__ == "__main__":
    sample_text = "你好，這是一段測試用的中文語音合成文本。希望能夠成功轉換成語音並儲存為 MP3 檔案！"
    azure_speech(sample_text)