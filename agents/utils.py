from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_core.runnables import Runnable

from utils import handle_err_and_raise


@handle_err_and_raise
def manage_llm_context_window(llm_agent: Runnable[LanguageModelInput, AIMessage], current_context: list[BaseMessage | SystemMessage]): return current_context