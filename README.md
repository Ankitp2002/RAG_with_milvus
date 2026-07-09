                  +-----------------------------+
                  |  Document Ingestion Router  |
                  +--------------+--------------+
                                 |
          +----------------------+----------------------+
          |                                             |
 +--------+---------------+                    +--------+------------+
 |  [Unstructured Data]   |                    |  [Structured Data]  |
 | (PDF, DOCX, TXT, etc.) |                    |  (CSV, XLSX, etc.)  |
 +--------+--------------+                     +--------+------------+
          |                                             |
 +--------+--------+                                    |
 | Docling Parser  |                             +------+------+
 +--------+--------+                             |   Pandas    |
          |                                      | Dataframe   |
 +--------+--------+                             +------+------+
 |   FastEmbed     |                                    |
 | (bge-large-v1.5)|                             +------+------+
 +--------+--------+                             | LangGraph   |
          |                                      | Filter Tool |
 +--------+--------+                             +------+------+
 | Milvus VectorDB |                                    |
 +--------+--------+                                    |
          |                                             |
          +----------------------+----------------------+
                                 |
                          +------+------+
                          | LangGraph   | <--- User Query
                          | Orchestration|
                          +------+------+
                                 |
                          +------+------+
                          |  Streamlit  |
                          |   UI View   |
                          +-------------+
                          
# Hybrid Advanced RAG System

A robust, enterprise-grade Retrieval-Augmented Generation (RAG) pipeline designed to seamlessly handle both **structured** (CSV, Excel) and **unstructured** (PDF, DOCX) documents.

By leveraging **Docling** for advanced document parsing, **LlamaIndex & Milvus** for unstructured vector search, and a dynamic **LangGraph & LangChain tool-binding architecture** for structured data filtering, this system bypasses traditional structured-to-vector data loss by querying dataframes directly via LLM-driven tools.

---
1. **Unstructured Pathway (PDF, DOCX):** Documents are parsed cleanly using IBM's `Docling`. Text is embedded using `BAAI/bge-large-en-v1.5` via LlamaIndex's `FastEmbedEmbedding` and indexed into a standalone **Milvus** vector database instance running via Docker.
2. **Structured Pathway (CSV, Excel):** Tabular documents completely bypass vector indexing. Instead, they are parsed via `Pandas` and tightly bound to the LLM agent as an interactive filtering and aggregation tool. The LLM intelligently generates filtering parameters or direct query translations to inspect tables with 100% precision.

## 🛠️ Tech Stack & Core Libraries

- **User Interface:** [Streamlit](https://streamlit.io/) — Fast, clean web interface for file uploading and real-time chat.
- **Orchestration Agent:** [LangGraph](https://www.langchain.com/langgraph) — State-machine-based workflow routing for predictable multi-turn agent logic.
- **LLM Application Layer:** [LangChain](https://www.langchain.com/) — For structural client definitions, prompt management, and tool bindings.
- **Data Parsing & Extraction:** [Docling](https://github.com/DS4SD/docling) — Layout-aware document parsing to respect hierarchies, lists, and native tables.
- **Vector Indexing & RAG Framework:** [LlamaIndex](https://www.llamaindex.ai/) — Used for data node chunking, embedding connections, and document structuring.
- **Vector Database:** [Milvus](https://milvus.io/) — High-performance, production-ready vector engine isolated via Docker Containers.
- **Embeddings:** `BAAI/bge-large-en-v1.5` via **FastEmbed** integration.
- **Data Manipulation:** [NumPy](https://numpy.org/) & [Pandas](https://pandas.pydata.org/) — In-memory processing and computational filtering for structured datasets.

---

## 📥 Prerequisites

Ensure you have the following installed on your machine:

- Python 3.12 wit uv
- Docker and Docker Compose

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/Ankitp2002/RAG_with_milvus.git]
cd RAG_with_milvus

bash milvus_db.sh

uv sync --link-mode=copy
vu run streamlit run app.py
```

_GROQ_API_KEY_="gsk..."
