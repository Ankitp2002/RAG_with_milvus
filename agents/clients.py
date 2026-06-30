from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# =====================================================================
# GROK Models
# =====================================================================
llm_gpt_oss_120 = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
llm_vision_llama_17b = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.3)
# =====================================================================

# =====================================================================
# Gemini Models
# =====================================================================
llm_gemini_2_5_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
# =====================================================================

# =====================================================================
# STARTUP LAYER: PRELOAD MODELS INTO MEMORY IMMEDIATELY
# =====================================================================
from docling.document_converter import DocumentConverter,PdfFormatOption, WordFormatOption, ExcelFormatOption, CsvFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableStructureOptions, PaginatedPipelineOptions
from docling.datamodel.base_models import InputFormat

print("📥 Preloading Docling Engines and RapidOCR Models into RAM...")
# =====================================================================

# =====================================================================
# PDF configuration
# =====================================================================
# Define structural pipeline parameters globally
pdf_pipeline_options = PdfPipelineOptions()
pdf_pipeline_options.do_table_structure = True
pdf_pipeline_options.do_ocr = True

# pdf_pipeline_options.do_code_enrichment = True
# pdf_pipeline_options.do_formula_enrichment = True

pdf_pipeline_options.images_scale = 2.0
pdf_pipeline_options.generate_page_images = True
pdf_pipeline_options.generate_picture_images = True
pdf_pipeline_options.generate_table_images = True

pdf_pipeline_options.generate_parsed_pages = True
pdf_pipeline_options.table_structure_options = TableStructureOptions(do_cell_matching=True)

pdf_strict_format_options = PdfFormatOption(pipeline_options=pdf_pipeline_options)
# =====================================================================

# =====================================================================
# DOCX configuration
# =====================================================================
# 1. Configure pipeline options
docx_pipeline_options = PaginatedPipelineOptions()
docx_pipeline_options.generate_picture_images=True
docx_pipeline_options.images_scale=2.0

word_strict_format_options = WordFormatOption(pipeline_options= docx_pipeline_options)
# =====================================================================

# =====================================================================
# EXCEL configuration
# =====================================================================
excel_strict_format_options = ExcelFormatOption() 
# =====================================================================

# =====================================================================
# Configuration all possible pipelines
# =====================================================================
format_to_options = {
    InputFormat.PDF: pdf_strict_format_options,
    InputFormat.DOCX: word_strict_format_options,
    InputFormat.XLSX: excel_strict_format_options,  
}

avl_pipeline = list(format_to_options.keys())
# =====================================================================

# =====================================================================
# Instantiate the single global converter instance
# =====================================================================
GLOBAL_CONVERTER = DocumentConverter(
    allowed_formats=avl_pipeline,
    format_options=format_to_options
)
for pipeline_init in avl_pipeline:
    GLOBAL_CONVERTER.initialize_pipeline(pipeline_init)
# =====================================================================