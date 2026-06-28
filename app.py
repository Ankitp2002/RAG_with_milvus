import warnings

import streamlit as st
import os
from langchain_core.messages import HumanMessage
from data_ingestion.file_processor import process_and_index_file
from pipeline import financial_bot_executor
from dotenv import load_dotenv
import logging

load_dotenv(override=True)

warnings.filterwarnings(
    "ignore", message=".*Accessing `__path__` from.*", category=UserWarning
)
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")
logging.getLogger("transformers").setLevel(logging.ERROR)

st.set_page_config(page_title="Financial Intelligence Agent", layout="wide")
st.title("📊 Production Financial Intelligence Chatbot Engine")

# 1. Initialize State Persistence across UI refreshes
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_registry" not in st.session_state:
    st.session_state.uploaded_registry = []
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# Sidebar: Controls, Language Overrides, and File Ingestion uploads
with st.sidebar:
    st.header("⚙️ Settings & Document Ingestion")

    # Multilingual Manual Override
    selected_lang = st.selectbox(
        "Conversation Language", ["en", "es", "fr", "de"], index=0
    )
    st.session_state.lang = selected_lang

    # File Uploader component
    uploaded_files = st.file_uploader(
        "Upload Financial Records",
        type=["csv", "xlsx", "pdf", "docx"],
        accept_multiple_files=True,
    )

    if st.button("Process Assets") and uploaded_files:
        for f in uploaded_files:
            temp_path = os.path.join("./tmp", f.name)
            os.makedirs("./tmp", exist_ok=True)
            with open(temp_path, "wb") as buffer:
                buffer.write(f.read())

            # Send file straight to LlamaIndex Ingestion Framework
            meta = process_and_index_file(temp_path)
            st.session_state.uploaded_registry.append(meta)
        st.success("All financial documents successfully parsed & indexed!")

# 2. Render Existing Chat Screen UI
for msg in st.session_state.messages:
    with st.chat_message(msg.type):
        st.write(msg.content)

# 3. Handle Active User Queries
if user_query := st.chat_input(
    "Ask a question about trends, summaries, or data sheets:"
):
    st.chat_message("user").write(user_query)

    # Save to standard history log
    new_human_msg = HumanMessage(content=user_query)
    st.session_state.messages.append(new_human_msg)

    # Package payload tracking parameters into LangGraph Initial State
    initial_graph_state = {
        "messages": st.session_state.messages,
        "active_files": st.session_state.uploaded_registry,
        "current_language": st.session_state.lang,
        "context_buffer": "",
    }

    # Run the hybrid compilation graph engine
    with st.spinner("Analyzing Financial Information..."):
        updated_state = financial_bot_executor.invoke(initial_graph_state)

    # Capture final answer response output from State Node
    final_response = updated_state["messages"][-1].content
    if isinstance(final_response, list):
        final_response = final_response[0]["text"]
        updated_state["messages"][-1].content = final_response

    st.session_state.messages.append(updated_state["messages"][-1])

    with st.chat_message("assistant"):
        st.markdown(final_response)
