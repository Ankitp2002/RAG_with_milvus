from langchain_core.tools import tool
from llama_index.vector_stores.milvus import MilvusVectorStore
from config import MILVUS_DB_URL
from sklearn.cluster import KMeans
import numpy as np
from utils import handle_err_and_raise


@tool
@handle_err_and_raise
def unstructured_summary(collection_name: str) -> str:
    """
    Use this tool ONLY when the user asks broad, global questions about the entire document,
    such as 'Summarize this PDF', 'What does this document hold?', or 'Give me an overview'.
    """
    vector_store = MilvusVectorStore(
        uri=MILVUS_DB_URL,
        collection_name=collection_name,
        dim=1024,
        overwrite=False,
    )
    milvus_client = vector_store.client

    all_vectors = []

    # 1. FIX: Initialize the official streaming QueryIterator
    iterator = milvus_client.query_iterator(
        collection_name=collection_name,
        filter="",  # Empty filter is completely legal here
        batch_size=10000,  # Pull data in efficient blocks of 1,000
        output_fields=["embedding"],
    )

    # 2. Safely consume the data stream until it runs dry
    while True:
        batch = iterator.next()
        if not batch:  # No more items left in the entire database
            break

        for item in batch:
            all_vectors.append(item["embedding"])

    # Always close your iterator connections when finished
    iterator.close()

    if not all_vectors:
        return "Collection contains no data to summarize."

    vectors = np.array(all_vectors)
    print(f"Successfully processed {len(vectors)} total vectors for clustering.")

    # 2. Dynamic Cluster Sizing
    # Find up to 5 distinct topic centers based on total data volume
    num_clusters = min(5, len(vectors))

    # 3. Run K-Means across the entire dataset
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
    kmeans.fit(vectors)
    centroids = kmeans.cluster_centers_

    summary_snippets = []
    search_params = {"metric_type": "IP", "params": {}}

    # 4. Search Milvus for the closest text snippet to EACH topic center
    for center_vector in centroids:
        search_nodes = milvus_client.search(
            collection_name=collection_name,
            data=[center_vector.tolist()],
            anns_field="embedding",
            search_params=search_params,
            limit=1,  # Grab the single most representative sentence for this group
            output_fields=["text"],
        )

    for hits in search_nodes:
        for hit in hits:
            summary_snippets.append(hit["entity"]["text"])

    # 5. Format output context strings safely
    core_context = "\n---\n".join(set(summary_snippets))
    return f"Here is a comprehensive summary covering the {num_clusters} main distinct topics found across all data segments:\n\n{core_context}"


@tool
@handle_err_and_raise
def structured_summary(summary_cache_path: str) -> str:
    """Extracts, aggregates, and summarizes ALL contents of a structured financial table or CSV file.

    Use this capability ONLY when the user requests a global overview, full data extraction,
    trend analysis, or a complete summary of structured/tabular data (like financial statements,
    spreadsheets, or balance sheets).

    Do NOT use this tool for single targeted row/cell lookups or quick specific metrics.

    Args:
        summary_cache_path (str): The exact collection_name or reference path associated
                                  with the target structured data asset.

    Returns:
        str: A comprehensive analytical summary of the structured data, or an error message.
    """
    # Your processing logic here
    return "structured_summary"
