import base64
from pathlib import Path

from utils import handle_err_and_log
from agents.clients import llm_vision_llama_17b
from langchain_core.messages import HumanMessage, AIMessage
from pathlib import Path
import base64

@handle_err_and_log
def get_grok_image_summary(image_path: Path) -> AIMessage:
    """Sends cropped images to Vision Model via OpenAI client SDK wrapper with dynamic extension handling."""
    
    ext = image_path.suffix.lower().lstrip(".")
    mime_type = "jpeg" if ext == "jpg" else ext

    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Describe this document image, chart, or diagram in detail for a RAG system search index. Explain trends, labels, and data points clearly."
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/{mime_type};base64,{encoded_image}", "detail": "high"}
            }
        ]
    )

    # Invoke using the standard LangChain interface
    return llm_vision_llama_17b.invoke([message])
