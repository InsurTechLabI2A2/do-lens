
"""AGENTE 1 - O Porteiro - Ingestor & OCR"""
from pathlib import Path
from pypdf import PdfReader
from typing import Tuple

class IngestorOCRAgent:
    """Recebimento dos documentos - Fluxo 1 + Extração bruta Fluxo 2"""
    def __init__(self, ocr_engine="pypdf"):
        self.ocr_engine = ocr_engine
    
    def processar(self, pdf_path: Path) -> Tuple[str, dict]:
        """Retorna texto bruto e metadados"""
        if not pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
        try:
            reader = PdfReader(str(pdf_path))
            textos = []
            for i, page in enumerate(reader.pages):
                try:
                    txt = page.extract_text() or ""
                    textos.append(f"\n--- PAGINA {i+1} ---\n{txt}")
                except Exception as e:
                    textos.append(f"\n--- PAGINA {i+1} ERRO OCR: {e} ---\n")
            texto_bruto = "\n".join(textos)
            meta = {
                "arquivo": str(pdf_path),
                "paginas": len(reader.pages),
                "ocr_engine": self.ocr_engine,
                "caracteres": len(texto_bruto),
                "confianca": 0.95 if len(texto_bruto) > 500 else 0.6
            }
            if meta["confianca"] < 0.8:
                meta["alerta"] = "Baixa confiança OCR - recomendar revisão humana"
            return texto_bruto, meta
        except Exception as ex:
            raise RuntimeError(f"Falha no OCR: {ex}")
