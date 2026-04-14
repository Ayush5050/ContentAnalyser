import os
import yt_dlp
import logging
from typing import Optional
from content_analyzer.utils.file_manager import FileManager

logger = logging.getLogger(__name__)

class InputHandler:
    @staticmethod
    async def download_video(url: str, download_dir: str) -> str:
        """
        Downloads video from URL using yt-dlp.
        Supports YouTube, Instagram, TikTok, etc.
        """
        output_template = os.path.join(download_dir, "video.%(ext)s")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
        }

        # Instagram fallback: use cookies from browser if possible
        # Note: In a production server, we might need a cookie file instead.
        if "instagram.com" in url:
            ydl_opts['cookiesfrombrowser'] = ('chrome',)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
                
                # Ensure it's named 'video.mp4' as expected by other modules
                final_path = FileManager.get_video_path(download_dir)
                if downloaded_file != final_path and os.path.exists(downloaded_file):
                    os.rename(downloaded_file, final_path)
                
                return final_path
        except Exception as e:
            logger.error(f"Error downloading video from {url}: {e}")
            raise RuntimeError(f"Failed to download video: {str(e)}")

    @staticmethod
    def handle_upload(file_content: bytes, download_dir: str) -> str:
        """Saves uploaded file content to the request directory."""
        video_path = FileManager.get_video_path(download_dir)
        with open(video_path, "wb") as f:
            f.write(file_content)
        return video_path
