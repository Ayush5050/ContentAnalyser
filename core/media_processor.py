import cv2
import os
import asyncio
import logging
import pytesseract
from typing import List, Tuple
from PIL import Image
from content_analyzer.config import settings
from content_analyzer.utils.file_manager import FileManager

logger = logging.getLogger(__name__)

class MediaProcessor:
    @staticmethod
    async def process_video(video_path: str, output_dir: str) -> Tuple[List[str], str, str]:
        """
        Runs frame extraction, audio stripping, and OCR in parallel.
        Returns: (list of frame paths, audio path, ocr_text)
        """
        audio_path = FileManager.get_audio_path(output_dir)
        frames_dir = FileManager.get_frames_dir(output_dir)

        # Run tasks in parallel
        results = await asyncio.gather(
            MediaProcessor.extract_frames(video_path, frames_dir),
            MediaProcessor.extract_audio(video_path, audio_path),
            MediaProcessor.run_ocr_pipeline(video_path),
            return_exceptions=True
        )

        frame_paths = results[0] if not isinstance(results[0], Exception) else []
        audio_out = audio_path if not isinstance(results[1], Exception) else ""
        ocr_text = results[2] if not isinstance(results[2], Exception) else ""

        if isinstance(results[0], Exception): logger.error(f"Frame extraction failed: {results[0]}")
        if isinstance(results[1], Exception): logger.error(f"Audio extraction failed: {results[1]}")
        if isinstance(results[2], Exception): logger.error(f"OCR failed: {results[2]}")

        return frame_paths, audio_out, ocr_text

    @staticmethod
    async def extract_frames(video_path: str, frames_dir: str) -> List[str]:
        """Extracts keyframes every N seconds."""
        frame_paths = []
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        interval = int(fps * settings.FRAME_EXTRACTION_INTERVAL)
        
        count = 0
        success = True
        while success:
            success, frame = cap.read()
            if success and count % interval == 0:
                frame_name = f"frame_{count}.jpg"
                frame_path = os.path.join(frames_dir, frame_name)
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
            count += 1
        cap.release()
        return frame_paths

    @staticmethod
    async def extract_audio(video_path: str, audio_path: str):
        """Strips audio using ffmpeg."""
        import subprocess
        try:
            cmd = [
                'ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', 
                '-ar', '16000', '-ac', '1', '-y', audio_path
            ]
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.wait()
        except Exception as e:
            logger.error(f"FFmpeg error: {e}")
            raise

    @staticmethod
    async def run_ocr_pipeline(video_path: str) -> str:
        """Runs OCR on every 5th extracted frame equivalent (simplified here to sampled frames)."""
        ocr_texts = []
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # We sample every 5 * interval frames for OCR
        interval = int(fps * settings.FRAME_EXTRACTION_INTERVAL * settings.OCR_FRAME_INTERVAL)
        
        count = 0
        success = True
        while success:
            success, frame = cap.read()
            if success and count % interval == 0:
                # Convert BGR to RGB for Tesseract
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                text = pytesseract.image_to_string(Image.fromarray(image))
                if text.strip():
                    ocr_texts.append(text.strip())
            count += 1
        cap.release()
        return " ".join(ocr_texts)
