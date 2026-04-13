from pydantic import BaseModel, Field
from typing import List, Optional

class AnalysisResponse(BaseModel):
    content_type: str = Field(..., description="movie_scene / news_event / sports / meme / music_video / unknown")
    title: str = Field(..., description="movie name or event name")
    context_summary: str = Field(..., description="2-3 sentence explanation")
    scene_detail: str = Field(..., description="what is happening in this specific clip")
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list, description="URLs from web search if used")
    language_detected: str = Field(..., description="Language detected in audio or text")

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
