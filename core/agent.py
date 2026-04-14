import logging
from typing import List, Dict, Any
from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool, tool
from content_analyzer.config import settings
from content_analyzer.tools.web_search import get_web_search_tool

logger = logging.getLogger(__name__)

class VideoContextAgent:
    def __init__(self):
        self.llm = Ollama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL
        )
        self.search_tool = get_web_search_tool()
    
    @tool
    def classify_content(query: str) -> str:
        """
        Classifies the content type of the video. 
        Possible values: movie_scene, news_event, sports_event, meme, music_video, unknown.
        """
        # This is a dummy implementation that the agent can call to 'confirm' its classification
        # In a real scenario, this might involve another LLM call or a specific classifier.
        return "Classification confirmed based on provided metadata."

    def _get_prompt(self):
        template = """You are a video context expert. Given visual scene description, 
audio transcript, and on-screen text from a short video video, 
identify the source (movie, TV show, news event, sports event etc.), 
explain what is happening, and provide full context. 

Input Metadata:
Visual Scene: {scene_description}
Audio Transcript: {transcript}
OCR Text: {ocr_text}

TOOLS:
------
You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response for the user, or if you have finished your analysis, please use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [Your detailed analysis here]
```

Begin!

Thought: {agent_scratchpad}"""
        return PromptTemplate.from_template(template)

    async def analyze(self, scene_description: str, transcript: str, ocr_text: str) -> str:
        tools = [self.search_tool, self.classify_content]
        prompt = self._get_prompt()
        agent = create_react_agent(self.llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        
        result = await agent_executor.ainvoke({
            "scene_description": scene_description,
            "transcript": transcript,
            "ocr_text": ocr_text,
            "agent_scratchpad": ""
        })
        
        return result["output"]
