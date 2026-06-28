from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ChatBotState(TypedDict):
    # Automatically manages and appends conversation history
    messages: Annotated[List[BaseMessage], add_messages]
    # Tracks currently uploaded tracking maps: [{"file_name": "...", "type": "structured|unstructured", "path": "..."}]
    active_files: List[Dict[str, str]]
    # Tracks session language dynamically ('en', 'es', 'fr')
    current_language: str
    # Shared clipboard for tools to deposit complex tabular context before generating final text
    context_buffer: str
