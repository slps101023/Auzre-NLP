from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.post("/analyze")
async def analyze(news_text: str):
    # Placeholder for actual analysis logic
    return {"analysis": f"Analyzed: {news_text}"}

@app.post("/crawler")
async def crawler(url: str):
    # Placeholder for actual crawling logic
    return {"crawled_data": f"Crawled data from: {url}"}