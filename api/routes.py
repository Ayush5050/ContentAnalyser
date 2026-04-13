import os
import logging
import asyncio
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from reelcontext.core.input_handler import InputHandler
from reelcontext.core.media_processor import MediaProcessor
from reelcontext.core.transcriber import Transcriber
from reelcontext.core.vision_router import VisionRouter
from reelcontext.core.agent import VideoContextAgent
from reelcontext.core.synthesizer import OutputSynthesizer
from reelcontext.utils.file_manager import FileManager
from reelcontext.schemas.output import AnalysisResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize singletons/reusable components
input_handler = InputHandler()
media_processor = MediaProcessor()
transcriber = Transcriber()
vision_router = VisionRouter()
context_agent = VideoContextAgent()
synthesizer = OutputSynthesizer()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if not url and not file:
        raise HTTPException(status_code=400, detail="Either url or file must be provided")

    request_dir = FileManager.create_request_dir()
    
    try:
        # Step 1: Input handling
        if file:
            content = await file.read()
            video_path = input_handler.handle_upload(content, request_dir)
        else:
            video_path = await input_handler.download_video(url, request_dir)

        # Step 2: Media Processing (Frames, Audio, OCR)
        frame_paths, audio_path, ocr_text = await media_processor.process_video(video_path, request_dir)

        # Step 3: Transcription
        transcript, language = await transcriber.transcribe(audio_path)

        # Step 4: Vision Analysis
        scene_description = await vision_router.get_scene_description(frame_paths, ocr_text)

        # Step 5: Agent reasoning
        agent_output = await context_agent.analyze(scene_description, transcript, ocr_text)

        # Step 6: Final Synthesis
        final_output = await synthesizer.synthesize(agent_output, language)
        
        return final_output

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temp directory
        FileManager.cleanup(request_dir)
