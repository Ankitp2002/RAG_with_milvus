# ==========================================
# 3. CORE PARSING & ENRICHMENT PIPELINE
# ==========================================
from docling_core.types.doc.document import (
    TableItem,
    PictureItem,
    TextItem,
    DocItemLabel,
)
from agents.clients import GLOBAL_CONVERTER
from utils import handle_err_and_raise
from agents.image_summary import get_grok_image_summary
from pathlib import Path
from llama_index.core import Document
import os

IMAGE_OUTPUT_DIR = Path("./extracted_images")
IMAGE_OUTPUT_DIR.mkdir(exist_ok=True)


@handle_err_and_raise
def pdf_parse_and_enrich_document(file_path: str) -> list[Document]:
    # 1. Convert the file safely
    result = GLOBAL_CONVERTER.convert(
        os.path.abspath(file_path), raises_on_error=False, page_range=(1, 5)
    )
    doc = result.document

    fig_counter = 0
    table_counter = 0

    # 2. Iterate over a snapshot list of items to allow in-place mutation
    for element, _level in list(doc.iterate_items()):
        if isinstance(element, (PictureItem, TableItem)):
            if (
                hasattr(element, "image")
                and element.image
                and hasattr(element.image, "pil_image")
            ):

                # Determine element type counters
                if isinstance(element, TableItem):
                    element_type = "table"
                    fig_index = table_counter
                    table_counter += 1
                else:
                    element_type = "fig"
                    fig_index = fig_counter
                    fig_counter += 1

                # Save visual crop element
                img_format = element.image.pil_image.format or "PNG"
                image_filename = f"{Path(file_path).stem}_{element_type}_{fig_index}.{img_format.lower()}"
                image_path = IMAGE_OUTPUT_DIR / image_filename

                with open(image_path, "wb") as f:
                    element.image.pil_image.save(f, format=img_format)

                print(
                    f"🖼️ Intercepting tag: Processing {element_type}_{fig_index} with Grok..."
                )
                summary = get_grok_image_summary(image_path)

                page_no = "Unknown"
                if hasattr(element, "prov") and element.prov:
                    page_no = getattr(element.prov[0], "page_no", "Unknown")

                # 3. Build the Markdown string block
                rich_markdown_replacement = (
                    f"\n\n"
                    f"### [Visual Data Asset: {element_type.upper()} {fig_index}]\n"
                    f"Local Source Reference Path: `{image_path.as_posix()}`\n"
                    f"Document Page Location: Page {page_no}\n"
                    f"Image Visual Content Analysis: {summary}\n"
                    f"### [End of Visual Data Asset]\n"
                    f"\n\n"
                )

                # 4. Create the TextItem structure
                new_text_item = TextItem(
                    self_ref=element.self_ref,  # Maintain its exact location pointer in the tree layout
                    parent=element.parent,
                    label=DocItemLabel.TEXT,
                    text=rich_markdown_replacement,
                    orig=rich_markdown_replacement,
                )

                # 5. IMMEDIATE MUTATION: Swap it into the tree instantly
                doc.replace_item(old_item=element, new_item=new_text_item)

    # 6. Export directly to Markdown
    markdown_text = doc.export_to_markdown()

    # Create clean unified LlamaIndex Document object
    llama_doc = Document(
        text=markdown_text,
        metadata={
            "file_name": Path(file_path).name,
            "total_extracted_images": fig_counter + table_counter,
        },
    )

    return [llama_doc]
