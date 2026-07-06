import pandas as pd
from utils import handle_err_and_raise


@handle_err_and_raise
def csv_parse_and_enrich_document(file_path: str) -> list:
    df = pd.read_csv(file_path)

    return [{"sheet_name": "default", "header": df.columns.tolist()}]
