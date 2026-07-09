from langchain_core.tools import tool
from utils import handle_err_and_raise
import pandas as pd


@tool
@handle_err_and_raise
def query_structured_docs(
    file_path: str, excel_query: dict[str, str] = {}, csv_query: str = ""
) -> dict:
    """
    Query structured documents from a pickle file.
    file_path: Path to the pickle file.
    excel_query: dict {sheet_name: query} for querying Excel files.
    csv_query: Pandas query string for querying CSV files.
    """
    df = pd.read_pickle(file_path)

    response_dict = {}
    if excel_query:
        excel_query_result_mapping = {}
        for sheet_name, query in excel_query.items():
            _df = df[sheet_name]
            _df = _df.query(query)
            excel_query_result_mapping[sheet_name] = _df.to_dict(orient="split")

        response_dict["data"] = excel_query_result_mapping

    elif csv_query:
        df = df.query(csv_query)
        response_dict["data"] = df.to_dict(orient="split")

    return response_dict
