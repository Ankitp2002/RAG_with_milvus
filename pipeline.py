import uuid

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from state import ChatBotState
from system_prompt_constant import SYSTEM_PROMPT
from tools.structured_tool import query_structured_docs
from tools.summary_tool import unstructured_summary, structured_summary
from tools.vector_rag_tool import query_unstructured_docs

# Import your other modular tools here...

from langchain_core.messages import AIMessage, SystemMessage
from agents.clients import llm_gpt_oss_120, llm_gemini_2_5_flash
from utils import handle_err_and_raise

# Register all modular LlamaIndex tools inside LangGraph bounds
tools_list = [
    query_unstructured_docs,
    query_structured_docs,
    unstructured_summary,
    # structured_summary,
]
tool_node = ToolNode(tools_list)


# Define the Master Supervisor Brain Node
@handle_err_and_raise
def financial_supervisor_agent(state: ChatBotState):
    # llm = llm_gemini_2_5_flash.bind_tools(tools_list)
    llm = llm_gpt_oss_120.bind_tools(tools_list)

    available_collections = [
        f"File: {f['file_name']} -> collection_name: {f.get('collection_name')}"
        for f in state["active_files"]
        if f["type"] == "unstructured"
    ]
    collections_context = (
        "\n".join(available_collections)
        if available_collections
        else "No files uploaded yet."
    )
    system_prompt = SYSTEM_PROMPT.format_map(
        {
            "current_language": state["current_language"],
            "collections_context": collections_context,
        }
    )

    formatted_messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(formatted_messages)
    return {"messages": [response]}


@handle_err_and_raise
def determine_next_node(state: ChatBotState):
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "execute_tools"
    return END


# Construct the State Machine Graph
workflow = StateGraph(ChatBotState)

workflow.add_node("supervisor", financial_supervisor_agent)
workflow.add_node("execute_tools", tool_node)

workflow.set_entry_point("supervisor")

# Router choice point
workflow.add_conditional_edges(
    "supervisor", determine_next_node, {"execute_tools": "execute_tools", END: END}
)

# Loop back to supervisor to digest data returned from LlamaIndex tool executions
workflow.add_edge("execute_tools", "supervisor")

# Compile production graph
financial_bot_executor = workflow.compile()
