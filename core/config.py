
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OCR_ENGINE = os.getenv("OCR_ENGINE", "pypdf")  # pypdf | azure | tesseract
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
