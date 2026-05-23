'use client';

import { useState, KeyboardEvent, useRef } from 'react';

export default function HomePage() {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [isUrlModalOpen, setIsUrlModalOpen] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);


  const handleProcess = async () => {
    if (!inputText.trim() || loading) return;

    const userMessage = inputText;
    // 先把使用者的輸入加入畫面，並清空輸入框
    setChatHistory((prev) => [...prev, { role: 'user', content: userMessage }]);
    setInputText('');
    setLoading(true);

    // 重置 textarea 高度
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
    if (isUrlModalOpen) {
      // 如果是網址模式，直接呼叫爬蟲 API
      try {
        const response = await fetch('http://localhost:8000/crawler', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: userMessage }),
        });
        const result = await response.json();
        setChatHistory((prev) => [...prev, { role: 'assistant', data: result }]);
      } catch (e) {
        console.error("處理失敗", e);
        setChatHistory((prev) => [...prev, { role: 'assistant', error: true }]);
      } finally {
        setLoading(false);
      }
    } else {
      try {
        // 呼叫 FastAPI 後端 (請確認後端正在執行)
        const response = await fetch('http://localhost:8000/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ news_text: userMessage }),
        });

        const result = await response.json();

        // 將 AI 的分析結果加入畫面
        setChatHistory((prev) => [...prev, { role: 'assistant', data: result }]);
      } catch (e) {
        console.error("處理失敗", e);
        setChatHistory((prev) => [...prev, { role: 'assistant', error: true }]);
      } finally {
        setLoading(false);
      }
    }

  };

  // 支援按 Enter 送出 (Shift+Enter 換行)
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleProcess();
    }
  };

  // 自動調整輸入框高度
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputText(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  // 在元件外部或內部定義一個小工具，用來轉換情緒的圖示與顏色
  const getSentimentStyle = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return { icon: '😊', text: '正向', color: 'bg-green-100 text-green-700 border-green-200' };
      case 'negative':
        return { icon: '😔', text: '負面', color: 'bg-red-100 text-red-700 border-red-200' };
      case 'mixed':
        // 📝 新增：處理正負情緒並存的情況
        return { icon: '🤔', text: '混合', color: 'bg-yellow-100 text-yellow-700 border-yellow-200' };
      case 'neutral':
      default:
        // 真正的毫無情緒或沒抓到狀態時才走這裡
        return { icon: '😐', text: '中立', color: 'bg-gray-100 text-gray-700 border-gray-200' };
    }
  };

  return (
    <div className="flex flex-col h-screen bg-white font-sans text-gray-800">

      {/* 1. 頂部標題列 (極簡設計) */}
      <header className="p-4 flex items-center justify-between">
        <h1 className="text-xl font-medium text-gray-700">CNN新聞分析台</h1>
      </header>

      {/* 2. 對話與結果顯示區 (可滾動) */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-8 scroll-smooth">
        <div className="max-w-3xl mx-auto space-y-8">

          {/* 預設迎賓訊息 */}
          {chatHistory.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full mt-20 space-y-4">
              <h2 className="text-4xl font-semibold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
                今天想分析哪則新聞？
              </h2>
              <p className="text-gray-500">貼上 CNN 等英文新聞內容，我會為您翻譯、補充維基百科並用語音播報。</p>
            </div>
          )}

          {/* 對話紀錄 */}
          {chatHistory.map((msg, index) => (
            <div key={index} className="animate-fade-in-up">
              {msg.role === 'user' ? (
                // 使用者輸入區塊
                <div className="flex justify-end">
                  <div className="bg-gray-100 rounded-2xl px-5 py-3 max-w-[80%] whitespace-pre-wrap text-gray-800">
                    {msg.content}
                  </div>
                </div>
              ) : (
                // AI 回覆區塊
                <div className="flex justify-start">
                  <div className="max-w-[90%] space-y-4">
                    {msg.error ? (
                      <p className="text-red-500">❌ 系統處理時發生錯誤，請稍後再試。</p>
                    ) : (
                      <div className="space-y-5 bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">

                        {/* 擴充 1：情緒分析徽章與語音播放器放在同一列 */}
                        <div className="flex flex-wrap items-center gap-3">
                          {msg.data.audio_url && (
                            <audio controls src={msg.data.audio_url} className="h-10 w-64" />
                          )}

                          {msg.data.sentiment && (
                            <span className={`px-3 py-1.5 rounded-full text-sm font-medium border flex items-center gap-1 ${getSentimentStyle(msg.data.sentiment.sentiment).color}`}>
                              <span>{getSentimentStyle(msg.data.sentiment.sentiment).icon}</span>
                              情緒分析：{getSentimentStyle(msg.data.sentiment.sentiment).text}
                            </span>
                          )}
                        </div>

                        {/* 擴充 2：重點摘要區塊 (特別凸顯) */}
                        {msg.data.summary && (
                          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
                            <h4 className="text-sm font-bold text-blue-800 mb-1">⚡ 重點速讀</h4>
                            <p className="text-gray-800 font-medium">{msg.data.summary}</p>
                          </div>
                        )}

                        {/* 原始中文翻譯 (字體稍微調淡，讓重點放在摘要上) */}
                        <div className="text-md leading-relaxed text-gray-600">
                          {msg.data.translated_text}
                        </div>

                        {/* 維基百科補充 */}
                        {msg.data.entities && msg.data.entities.length > 0 && (
                          <div className="mt-4 pt-4 border-t border-gray-100">
                            <h4 className="text-sm font-medium text-gray-500 mb-3 flex items-center gap-2">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                              關鍵字補充
                            </h4>
                            <div className="flex flex-wrap gap-2">
                              {msg.data.entities.map((entity: any, i: number) => (
                                <a
                                  key={i} href={entity.url} target="_blank" rel="noopener noreferrer"
                                  className="inline-flex items-center px-3 py-1.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-blue-600 hover:bg-blue-50 transition-colors"
                                >
                                  {entity.name} ↗
                                </a>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* 載入中動畫 */}
          {loading && (
            <div className="flex justify-start animate-pulse">
              <div className="flex gap-2 items-center text-blue-500 font-medium bg-blue-50 px-4 py-2 rounded-2xl">
                <span className="flex gap-1">
                  <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                  <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                  <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                </span>
                正在分析新聞與生成語音...
              </div>
            </div>
          )}
        </div>
      </main>

      {/* 3. 置底輸入框 (Gemini 風格) */}
      <footer className="p-4 w-full max-w-3xl mx-auto mb-4">
        <div className="relative flex flex-col bg-[#f0f4f9] rounded-[24px] p-2 focus-within:ring-1 focus-within:ring-gray-300 transition-all shadow-sm">
          <textarea
            ref={textareaRef}
            value={inputText}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
            placeholder={isUrlModalOpen ? "請輸入新聞網址 (按 Enter 送出)" : "在此貼上英文新聞 (按 Enter 送出)"}
            className="w-full bg-transparent resize-none outline-none px-4 py-3 max-h-48 text-gray-800 placeholder-gray-500"
            rows={1}
          />

          <div className="flex justify-between items-center px-2 pb-1">
            {/* 左側可擴充功能 (例如加入附件的按鈕) */}
            <div className="text-gray-400 flex items-center gap-1">
              <button
                type="button" // 預防表單重整
                className={`p-2 hover:bg-gray-100 rounded-full transition relative ${inputText ? 'text-blue-500 bg-blue-50' : ''}`}
                title={inputText ? `已鎖定網址: ${inputText}` : "輸入新聞網址分析"}
                onClick={(e) => {
                  e.preventDefault();
                  isUrlModalOpen ? setIsUrlModalOpen(false) : setIsUrlModalOpen(true);
                }}
              >
                <svg className="w-5 h-5 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                </svg>
              </button>

              {/* 確保這個提示字在按鈕外面，點擊它不會干擾按鈕 */}
              {isUrlModalOpen && (
                <span className="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-md max-w-[100px] truncate select-none">
                  🔗 已帶入
                </span>
              )}
            </div>

            {/* 右側送出按鈕 */}
            <button
              onClick={handleProcess}
              disabled={!inputText.trim() || loading}
              className={`p-2 rounded-full transition-colors ${inputText.trim() && !loading
                ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-md'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                }`}
            >
              <svg className="w-5 h-5 transform rotate-90" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"></path>
              </svg>
            </button>
          </div>
        </div>
        <p className="text-center text-xs text-gray-400 mt-3">
          AI 可能會產生不準確的資訊，請斟酌參考維基百科連結。
        </p>
      </footer>

    </div>
  );
}