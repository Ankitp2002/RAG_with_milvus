import os

from langchain_core.tools import tool
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.milvus import MilvusVectorStore
from config import MILVUS_DB_URL
from utils import handle_err_and_raise


# Ensure your Settings.embed_model is configured to output 1024 dims globally in config.py
@tool
@handle_err_and_raise
def query_unstructured_docs(query_str: str, collection_name: str) -> str:
    """
    Searches an unstructured financial document collection inside the Milvus
    database file to retrieve relevant context, metrics, and report details.
    """
    vector_store = MilvusVectorStore(
        uri=MILVUS_DB_URL,
        collection_name=collection_name,
        dim=1024,  # Must perfectly match the embedding model used during ingestion
        overwrite=False,  # Critical: Keep false so you don't clear the data
    )

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    query = index.as_retriever(similarity_top_k=4, streaming=True)

    response = query.retrieve(query_str)
    context_text = "\n\n".join([node.node.get_content() for node in response])

    return context_text
