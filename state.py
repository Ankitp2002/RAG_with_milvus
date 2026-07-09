from typing import Annotated, List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ChatBotState(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)  # History
    active_files: list = Field(default_factory=list) # uploaded file
    current_language: str = "en" # selected language
    context_buffer: str = "" #
    selected_llm: str = Field(default="llm_gpt_oss_120")
