from pydantic import BaseModel

class InputSchema(BaseModel):
    tool_name: str = "search_news_tool"
    query: str
    location: str = None
    date: str = None