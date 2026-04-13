import logging
import uvicorn
from fastapi import FastAPI
from reelcontext.api.routes import router
from reelcontext.config import settings

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="ReelContext API",
    description="AI agent for identifying movie scenes and real-world events from short-form videos.",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("reelcontext.main:app", host="0.0.0.0", port=8000, reload=True)
