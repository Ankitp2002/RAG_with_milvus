from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# =====================================================================
# GROK 
llm_gpt_oss_120 = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
llm_vision_llama_17b = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.3)

# Gemini
llm_gemini_2_5_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
# =====================================================================

from docling.document_converter import DocumentConverter,PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableStructureOptions
from docling.datamodel.base_models import InputFormat
# =====================================================================
# 1. STARTUP LAYER: PRELOAD MODELS INTO MEMORY IMMEDIATELY
# =====================================================================
print("📥 Preloading Docling Engines and RapidOCR Models into RAM...")

# Define structural pipeline parameters globally
pipeline_options = PdfPipelineOptions()
pipeline_options.do_table_structure = True
pipeline_options.do_ocr = True

# pipeline_options.do_code_enrichment = True
# pipeline_options.do_formula_enrichment = True

pipeline_options.images_scale = 2.0
pipeline_options.generate_page_images = True
pipeline_options.generate_picture_images = True
pipeline_options.generate_table_images = True

pipeline_options.generate_parsed_pages = True
pipeline_options.table_structure_options = TableStructureOptions(do_cell_matching=True)

strict_format_options = PdfFormatOption(pipeline_options=pipeline_options)
format_to_options = {
    InputFormat.PDF: strict_format_options,
    # InputFormat.IMAGE: strict_format_options,
    # InputFormat.DOCX: strict_format_options,
    # InputFormat.PPTX: strict_format_options
}

avl_pipeline = list(format_to_options.keys())
# Instantiate the single global converter instance instance
GLOBAL_CONVERTER = DocumentConverter(
    allowed_formats=avl_pipeline,
    format_options=format_to_options
)
for pipeline_init in avl_pipeline:
    GLOBAL_CONVERTER.initialize_pipeline(pipeline_init)