# ContentAnalyzer Project Roadmap

ContentAnalyzer is an AI-powered agent designed to take short-form videos (Instagram, YouTube Shorts, TikTok) and identify their origin (movie scenes, real-world events, memes) and provide full context.

## 🎯 Project Goal
To build a production-level, multi-modal AI pipeline that can "see" and "hear" short-form content to identify it and explain it to the user with high accuracy and retrieved context from the web.

## ✅ What We've Built So Far

### 1. Core Processing Pipeline
- **Parallel Media Extraction**: Rapidly extracts keyframes (OpenCV), strips audio (FFmpeg), and runs OCR (Tesseract) in parallel using `asyncio`.
- **Audio Transcription**: Integrated OpenAI Whisper (small model) for high-accuracy speech-to-text.
- **Dynamic Vision Routing**: A router that intelligently chooses between GPT-4o (for detail/complex scenes) and Gemini 1.5 Flash (for text-heavy/news content).

### 2. Intelligent Reasoning Agent
- **Orchestration**: LangChain-based agent using a local LLM (Ollama - Llama 3.1 8B).
- **Web Retrieval**: Integration with DuckDuckGo for real-time verification of film titles or news dates.
- **Content Classification**: Specialized tool for identifying content categories (movie, news, sports, etc.).

### 3. API & Infrastructure
- **REST API**: FastAPI endpoints for `/analyze` (URL or file upload) and `/health`.
- **Config Management**: Pydantic `BaseSettings` for environment variable handling.
- **Version Control**: Full Git history and GitHub repository sync.

---

## 🚀 What's Left / Planned Features

### Phase 1: Refining Accuracy (Priority)
- [ ] **Advanced Vision Prompting**: Improve few-shot prompting for the vision models.
- [ ] **IMDb/TMDB Integration**: Add specialized tools for the agent to query movie databases directly.
- [ ] **Metadata Scraping**: Extract video titles and descriptions from platforms (yt-dlp) to feed as extra context to the agent.

### Phase 2: Performance & Scalability
- [ ] **Dockerization**: Create a containerized environment for easier deployment.
- [ ] **Async Worker Queue**: Move heavy video processing to Celery/Redis for handling concurrent requests.
- [ ] **Video Segmenting**: Handle longer videos by analyzing them in segments.

### Phase 3: User Experience
- [ ] **Web UI**: Build a simple React/Next.js frontend for video analysis.
- [ ] **Streaming Responses**: Implement Server-Sent Events (SSE) to show the agent's "thinking" process in real-time.
- [ ] **Export to Notion/Obsidian**: Allow users to save analyzed context to their digital brains.

---

## 🛠️ Contribution
This project is currently in active development. Please refer to the [walkthrough.md](walkthrough.md) for local setup instructions.
