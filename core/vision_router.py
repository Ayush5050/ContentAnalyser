import base64
import logging
import os
from typing import List
from openai import OpenAI
import google.generativeai as genai
from reelcontext.config import settings

logger = logging.getLogger(__name__)

class VisionRouter:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def get_scene_description(self, frame_paths: List[str], ocr_text: str) -> str:
        """
        Routes description task to GPT-4o or Gemini based on content.
        """
        # Pick max 5 evenly spaced frames
        frames_to_use = []
        if frame_paths:
            n = len(frame_paths)
            indices = [int(i * (n - 1) / (settings.MAX_VISION_FRAMES - 1)) for i in range(min(n, settings.MAX_VISION_FRAMES))] if n > 1 else [0]
            frames_to_use = [frame_paths[idx] for idx in indices]

        # Basic routing logic: If frames contain mostly text/news (based on OCR length) → use Gemini
        # Otherwise use GPT-4o
        use_gemini = len(ocr_text) > 200 or "news" in ocr_text.lower() or "report" in ocr_text.lower()

        try:
            if use_gemini:
                return await self._call_gemini(frames_to_use)
            else:
                return await self._call_gpt4o(frames_to_use)
        except Exception as e:
            logger.warning(f"Primary vision model failed: {e}. Falling back...")
            # Fallback
            try:
                if use_gemini:
                    return await self._call_gpt4o(frames_to_use)
                else:
                    return await self._call_gemini(frames_to_use)
            except Exception as e2:
                logger.error(f"Fallback vision model also failed: {e2}")
                return "Vision analysis failed."

    async def _call_gpt4o(self, frame_paths: List[str]) -> str:
        logger.info("Calling GPT-4o Vision...")
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the scene in these video frames. Identify any movies, actors, or real-world events shown."},
                    *[
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{self._encode_image(fp)}"}
                        }
                        for fp in frame_paths
                    ]
                ]
            }
        ]
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=500
        )
        return response.choices[0].message.content

    async def _call_gemini(self, frame_paths: List[str]) -> str:
        logger.info("Calling Gemini 1.5 Flash Vision...")
        parts = ["Describe the scene in these video frames. Identify any movies, actors, or real-world events shown."]
        for fp in frame_paths:
            with open(fp, "rb") as f:
                img_data = f.read()
                parts.append({"mime_type": "image/jpeg", "data": img_data})
        
        response = self.gemini_model.generate_content(parts)
        return response.text
