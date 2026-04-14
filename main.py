import logging
import uvicorn
from fastapi import FastAPI
from content_analyzer.api.routes import router
from content_analyzer.config import settings

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="ContentAnalyzer API",
    description="AI agent for identifying movie scenes and real-world events from short-form videos.",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("content_analyzer.main:app", host="0.0.0.0", port=8000, reload=True)
