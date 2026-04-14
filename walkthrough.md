# ContentAnalyzer Walkthrough

ContentAnalyzer is an AI-powered agent for identifying movie scenes, news events, and more from short-form videos. It combines computer vision, audio transcription, and local LLM reasoning to provide deep context.

## 🛠️ Tech Stack & Features
- **FastAPI**: REST API backend.
- **yt-dlp**: Seamless download from YouTube, Instagram, and TikTok.
- **Parallel Processing**: Async processing of keyframes (OpenCV), audio (FFmpeg), and OCR (Tesseract).
- **Multi-Modal Vision**: Intelligently routes between GPT-4o and Gemini 1.5 Flash.
- **Agentic Reasoning**: LangChain with Ollama (Llama 3.1) and DuckDuckGo search.

## 📁 Project Structure
```text
content_analyzer/
├── main.py              # Entry point
├── config.py            # Global settings
├── api/
│   └── routes.py        # POST /analyze
├── core/
│   ├── agent.py         # LangChain logic
│   ├── vision_router.py # Dual-LLM vision routing
│   ├── media_processor.py # Parallel processing pipeline
│   ├── ...
├── tools/
│   └── web_search.py    # DuckDuckGo wrapper
└── schemas/
    └── output.py        # Pydantic response schema
```

## 🚀 Getting Started

### 1. Requirements
Ensure you have the following installed:
- FFmpeg
- Tesseract OCR
- Ollama (running `llama3.1:8b`)

### 2. Installation & Setup
I have already installed the Python dependencies. To set up the remaining system tools, please run this command in your terminal:

```bash
# Install system tools via Brew
brew install ffmpeg tesseract yt-dlp

# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the required model
ollama pull llama3.1:8b
```

Then, configure your `.env` file:
```bash
cp .env.example .env
# Add your OPENAI_API_KEY and GOOGLE_API_KEY
```

### 3. Run the API
```bash
python main.py
```

## 🧪 Usage Examples

### Analyze a YouTube Short
```bash
curl -X POST http://localhost:8000/analyze \
  -F "url=https://youtube.com/shorts/..."
```

### Analyze an Uploaded Video
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@/path/to/my_video.mp4"
```

## 📦 Output Schema
The API returns a structured JSON:
```json
{
  "content_type": "movie_scene",
  "title": "Interstellar",
  "context_summary": "This clip shows the docking scene where character Cooper...",
  "scene_detail": "High-intensity scene with dramatic music and Hans Zimmer score...",
  "confidence": 0.95,
  "sources": ["https://en.wikipedia.org/wiki/Interstellar_(film)"],
  "language_detected": "en"
}
```

---

> [!NOTE]
> The project uses `/tmp/content_analyzer` for temporary file storage and automatically cleans up after every request.
