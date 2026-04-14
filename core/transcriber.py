import whisper
import logging
from typing import Tuple
from content_analyzer.config import settings

logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            logger.info(f"Loading Whisper {settings.WHISPER_MODEL} model...")
            self.model = whisper.load_model(settings.WHISPER_MODEL)

    async def transcribe(self, audio_path: str) -> Tuple[str, str]:
        """
        Transcribes audio file and detects language.
        Returns: (transcript, language_code)
        """
        try:
            self.load_model()
            result = self.model.transcribe(audio_path)
            transcript = result.get("text", "").strip()
            language = result.get("language", "unknown")
            return transcript, language
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            return "", "unknown"
