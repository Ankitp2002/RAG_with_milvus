from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from state import ChatBotState

def financial_supervisor_agent(state: ChatBotState):
    # Extract only the unstructured file collections currently available in memory
    available_collections = [
        f"File: {f['file_name']} -> collection_name: {f.get('collection_name')}"
        for f in state["active_files"] if f["type"] == "unstructured"
    ]
    
    # Inject the Milvus system mapping directly into the LLM context prompt
    system_prompt = (
        f"You are an Advanced Financial Intelligence Supervisor. Current Language: {state['current_language']}.\n"
        f"Available Document Collections in Milvus DB:\n{', '.join(available_collections)}\n\n"
        "Examine the query. If searching an unstructured PDF/Docx, invoke `query_unstructured_financial_docs` "
        "and make sure you copy the exact `collection_name` for that specific file from the list above into the arguments."
    )
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    # registers tool list cleanly
    from tools.vector_rag_tool import query_unstructured_financial_docs
    llm_with_tools = llm.bind_tools([query_unstructured_financial_docs])
    
    messages_with_system = [{"role": "system", "content": system_prompt}] + state["messages"]
    response = llm_with_tools.invoke(messages_with_system)
    
    return {"messages": [response]}
