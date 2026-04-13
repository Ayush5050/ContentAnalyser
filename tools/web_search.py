from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

def get_web_search_tool():
    search = DuckDuckGoSearchRun()
    return Tool(
        name="web_search",
        func=search.run,
        description="Search the web for information about movies, news events, or entities mentioned in the video context. Use this when you are unsure about the identification."
    )
