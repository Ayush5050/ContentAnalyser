import json
import logging
from typing import Dict, Any
from langchain_community.llms import Ollama
from content_analyzer.config import settings
from content_analyzer.schemas.output import AnalysisResponse

logger = logging.getLogger(__name__)

class OutputSynthesizer:
    def __init__(self):
        self.llm = Ollama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL
        )

    async def synthesize(self, agent_output: str, language_detected: str) -> AnalysisResponse:
        """
        Uses LLM to parse unstructured agent output into structured Pydantic schema.
        """
        prompt = f"""
        Extract the following information from the video analysis report provided below and return it strictly as a JSON object.
        
        Fields required:
        - content_type: (movie_scene / news_event / sports / meme / music_video / unknown)
        - title: (movie name or event name)
        - context_summary: (2-3 sentence explanation)
        - scene_detail: (what is happening in this specific clip)
        - confidence: (float 0.0 to 1.0)
        - sources: (list of URLs mentioned if any)

        Analysis Report:
        {agent_output}

        JSON Output:
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            # Try to strip any potential markdown formatting
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3]
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3]
            
            data = json.loads(clean_response)
            data["language_detected"] = language_detected
            
            return AnalysisResponse(**data)
        except Exception as e:
            logger.error(f"Error synthesizing output: {e}")
            # Fallback with partial data
            return AnalysisResponse(
                content_type="unknown",
                title="Analysis Error",
                context_summary="Failed to parse structured output from agent.",
                scene_detail=agent_output[:500],
                confidence=0.1,
                sources=[],
                language_detected=language_detected
            )
