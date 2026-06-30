# ==========================================
# 3. CORE PARSING & ENRICHMENT PIPELINE
# ==========================================
import pandas as pd

from utils import handle_err_and_raise
from pathlib import Path
from llama_index.core import Document
from config import STRUCTURED_DOCUMENT_CONVERT_CHUNK_SIZE

@handle_err_and_raise
def csv_parse_and_enrich_document(file_path: str) -> list[Document]:
    print("📊 Processing CSV file via high-performance chunk streaming...")
        
    # Get total rows quickly without RAM exhaustion
    total_rows = sum(1 for _ in open(file_path, 'r', encoding='utf-8', errors='ignore')) - 1
    
    current_row = 1
    final_full_markdown = []
    # Loop through CSV 50K rows at a time
    for chunk_df in pd.read_csv(file_path, chunksize=STRUCTURED_DOCUMENT_CONVERT_CHUNK_SIZE, low_memory=True):
        end_row = min(current_row + len(chunk_df) - 1, total_rows)
        print(f"⏳ Processing row window: Rows {current_row:,} to {end_row:,}...")
        
        # Convert this 50K chunk block into a clean Markdown table string
        chunk_markdown = chunk_df.to_markdown(index=False)
        final_full_markdown.append(chunk_markdown)
        
        table_counter += 1
        current_row += len(chunk_df)
    
    # Create the final unified LlamaIndex Document object
    llama_doc = Document(
        text=final_full_markdown,
        metadata={
            "file_name": Path(file_path).name,
            "file_type": file_path,
            "total_extracted_tables": table_counter,
            "total_rows_processed": total_rows
        },
    )
    
    return [llama_doc]
