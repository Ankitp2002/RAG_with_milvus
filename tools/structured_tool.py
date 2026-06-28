from langchain_core.tools import tool
from utils import handle_err_and_raise


@tool
@handle_err_and_raise
def query_structured_docs(query_str: str, collection_name: str) -> str:
    """Executes a targeted search or specific lookup query against a structured data table or CSV file.

    Use this capability ONLY when the user asks for a specific metric, row lookup, cell value,
    or filtered data point from tabular datasets (e.g., 'What was the net profit in 2023?',
    'Find the row for marketing expenses').

    Do NOT use this tool if the user wants a broad overview, general trend analysis, or wants to
    summarize/extract the entire file.

    Args:
        query_str (str): The specific question or search criteria requested by the user.
        collection_name (str): The exact collection identifier associated with the target structured asset.

    Returns:
        str: The extracted structured data rows/cells matching the query, or an error message.
    """
    return "query_structured_docs"
