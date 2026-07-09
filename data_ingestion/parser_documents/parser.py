import gc
from typing import Union

from docling_core.types.doc.document import (
    TableItem,
    PictureItem,
    TextItem,
    DocItemLabel,
)
from agents.image_summary import get_grok_image_summary
from agents.clients import GLOBAL_CONVERTER
from pathlib import Path

IMAGE_OUTPUT_DIR = Path("./extracted_images")
IMAGE_OUTPUT_DIR.mkdir(exist_ok=True)

def replace_image_table_with_summary(doc, element, table_counter, fig_counter, abs_path) -> tuple[int, ...]:
    # Maintain correct index across chunks
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
    image_filename = f"{Path(abs_path).stem}_{element_type}_{fig_index}.{img_format.lower()}"
    image_path = IMAGE_OUTPUT_DIR / image_filename
    
    with open(image_path, "wb") as f:
        element.image.pil_image.save(f, format=img_format)
        
    print(f"🖼️ Intercepting tag: Processing {element_type}_{fig_index} with Grok...")
    summary = get_grok_image_summary(image_path)
    
    page_no = "Unknown"
    if hasattr(element, "prov") and element.prov:
        page_no = getattr(element.prov[0], "page_no", "Unknown")
        
    # Build replacement string block
    rich_markdown_replacement = (
        f"\n\n"
        f"### [Visual Data Asset: {element_type.upper()} {fig_index}]\n"
        f"Local Source Reference Path: `{image_path.as_posix()}`\n"
        f"Document Page Location: Page {page_no}\n"
        f"Image Visual Content Analysis: {summary}\n"
        f"### [End of Visual Data Asset]\n"
        f"\n\n"
    )
    
    new_text_item = TextItem(
        self_ref=element.self_ref,
        parent=element.parent,
        label=DocItemLabel.TEXT,
        text=rich_markdown_replacement,
        orig=rich_markdown_replacement,
    )
    
    # Mutate tree segment
    doc.replace_item(old_item=element, new_item=new_text_item)
    
    # Close image stream immediately to drop RAM footprint
    element.image.pil_image.close()
    return fig_counter, table_counter

def get_mark_down(abs_path:str, start_page:int, end_page:int, table_counter:int, fig_counter:int) -> tuple[str, int, int]:
    # Pull only this tiny section into RAM
    result = GLOBAL_CONVERTER.convert(
        abs_path, 
        raises_on_error=False, 
        page_range=(start_page, end_page)
    )
    
    doc = result.document
    
    if not result or not result.document:
        return doc.export_to_markdown()
        
    # 3. Snapshot loop for safe item mutation within the chunk
    for element, _level in list(doc.iterate_items()):
        if isinstance(element, (PictureItem, TableItem)):
            if (
                hasattr(element, "image")
                and element.image
                and hasattr(element.image, "pil_image")
            ):
                fig_counter, table_counter = replace_image_table_with_summary(doc, element, table_counter, fig_counter, abs_path)
    
    markdown = doc.export_to_markdown()
    
    del result
    del doc
    gc.collect()
    
    return markdown, fig_counter, table_counter