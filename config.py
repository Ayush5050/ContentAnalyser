from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GOOGLE_API_KEY: str
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"
    LOG_LEVEL: str = "INFO"
    
    # Media Processing Settings
    FRAME_EXTRACTION_INTERVAL: int = 2  # Extract frame every N seconds
    OCR_FRAME_INTERVAL: int = 5        # Run OCR on every Nth extracted frame
    MAX_VISION_FRAMES: int = 5         # Max frames to send to Vision LLM
    WHISPER_MODEL: str = "small"
    
    # Directories
    BASE_TEMP_DIR: str = "/tmp/content_analyzer"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
