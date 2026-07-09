import os
from pathlib import Path
from typing import List
from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from utils import handle_err_and_raise
from .parser_documents.pdf_parser import pdf_parse_and_enrich_document
from .parser_documents.docx_parser import docx_parse_and_enrich_document
from .parser_documents.csv_parser import csv_parse_and_enrich_document
from .parser_documents.excel_parser import excel_parse_and_enrich_document
from config import MILVUS_DB_URL, TEMP_DIR

Settings.embed_model = FastEmbedEmbedding(
    model_name="BAAI/bge-large-en-v1.5", cache_dir="./fastembed_cache"
)  # Embedding Model
Settings.llm = None


@handle_err_and_raise
def process_and_index_file(file_path: str) -> dict:
    """
    Ingests and routes files. If unstructured, extracts chunks and
    stores their embeddings directly into an enterprise Milvus collection.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    file_name = os.path.basename(file_path)

    # 1. Structured Data Engine (CSV/Excel)
    if ext in [".csv", ".xlsx", ".xls"]:
        file_name = f"{TEMP_DIR}/{file_name.split('.')[0]}.pkl"
        if ext == ".csv":
            meta_info = csv_parse_and_enrich_document(file_path, file_name)  # CSV
        else:
            meta_info = excel_parse_and_enrich_document(file_path, file_name)  # Excel

        return {
            "file_name": file_name,
            "type": "structured",
            "format": ext,
            "collection_name": None,
            "meta_info": meta_info,
        }

    # 2. Unstructured Data Engine (PDF/DOCX -> LlamaIndex -> Milvus)
    else:

        documents = layout_aware_parsing_engin(os.path.normpath(file_path))

        # Format a clean, valid collection name for Milvus (alphanumeric and underscores only)
        collection_name = (
            "fin_" + "".join([c if c.isalnum() else "_" for c in file_name]).lower()
        )

        # ----------- for validation is it correct way to conversion of unstructured to raw text
        for_validation_save_as_markdown(documents, file_name.split(".")[0])
        # -----------

        text_embedding_vector_storing(collection_name, documents)
        return {
            "file_name": file_name,
            "collection_name": collection_name,
            "type": "unstructured",
            "format": ext,
        }


@handle_err_and_raise
def layout_aware_parsing_engin(file_path: str) -> list[Document]:
    """convert all unstructured files to markdown formate for vectorization"""
    file_exe = file_path.split(".")[-1].lower()
    documents = [Document()]

    if file_exe == "pdf":
        documents = pdf_parse_and_enrich_document(file_path)  # PDF

    if file_exe == "docx":
        documents = docx_parse_and_enrich_document(file_path)  # DOCX

    return documents


@handle_err_and_raise
def text_embedding_vector_storing(collection_name, documents: List[Document]) -> None:
    """Store text as vector into milvus vectorDB which is batter for production application"""
    # Initialize LlamaIndex's Milvus Storage Store
    vector_store = MilvusVectorStore(
        uri=MILVUS_DB_URL,  # local DB | we can add dedicated container as well
        collection_name=collection_name,
        dim=1024,  # Matches with embedding mode vectors dimensions ((we can also use standard OpenAI text-embedding-3-small or text-davinci dimensions))
        overwrite=True,
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )  # Storing Vectors


@handle_err_and_raise
def for_validation_save_as_markdown(documents, file_name):
    """Validate Unstructured data convert appropriate (image as summary, table as markdown table among other) or not"""
    # Extract the parsed text content
    parsed_text = "\n\n".join([doc.text for doc in documents])
    
    markdown_dir = Path("./validate_doc_md")
    markdown_dir.mkdir(exist_ok=True)
    
    # 1. Save as Markdown (.md) to check original structure
    md_path = f"{markdown_dir}/{file_name}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(parsed_text)

    print(f"Markdown verification file saved to: {md_path}")
