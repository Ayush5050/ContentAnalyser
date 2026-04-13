import os
import shutil
import uuid
from typing import Generator
from reelcontext.config import settings

class FileManager:
    @staticmethod
    def create_request_dir() -> str:
        """Creates a unique temporary directory for a request."""
        request_id = str(uuid.uuid4())
        path = os.path.join(settings.BASE_TEMP_DIR, request_id)
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def cleanup(dir_path: str):
        """Removes the temporary directory and all its contents."""
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def get_video_path(dir_path: str) -> str:
        return os.path.join(dir_path, "reel.mp4")

    @staticmethod
    def get_audio_path(dir_path: str) -> str:
        return os.path.join(dir_path, "audio.wav")

    @staticmethod
    def get_frames_dir(dir_path: str) -> str:
        frames_dir = os.path.join(dir_path, "frames")
        os.makedirs(frames_dir, exist_ok=True)
        return frames_dir
