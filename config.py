# Docker container
MILVUS_DB_URL = "http://127.0.0.1:19530"

# Define a safe chunk window (e.g., 5 pages at a time to prevent RAM spikes)
UNSTRUCTURED_UNSTRUCTURED_DOCUMENT_CONVERT_CHUNK_SIZE = 5
STRUCTURED_DOCUMENT_CONVERT_CHUNK_SIZE = 50000
