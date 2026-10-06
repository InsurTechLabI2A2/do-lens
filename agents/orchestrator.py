
"""Orquestrador LangGraph - Integração dos 5 agentes"""
from agents.ingestor_ocr import IngestorOCRAgent
from agents.extractor import ExtractorAgent
from agents.normalizer import NormalizerAgent
from agents.comparator import ComparatorAgent
from agents.reporter import ReporterAgent
from pathlib import Path

class DOLensOrchestrator:
    def __init__(self):
        self.ingestor = IngestorOCRAgent()
        self.extractor = ExtractorAgent(use_mock=True)
        self.normalizer = NormalizerAgent()
        self.comparator = ComparatorAgent()
        self.reporter = ReporterAgent()
    
    def processar_apolice(self, pdf_path: Path):
        texto, meta = self.ingestor.processar(pdf_path)
        estruturada = self.extractor.extrair(texto, meta)
        normalizada = self.normalizer.normalizar(estruturada)
        return normalizada, meta, texto
    
    def comparar_apolices(self, path_a: Path, path_b: Path):
        apolice_a, meta_a, _ = self.processar_apolice(path_a)
        apolice_b, meta_b, _ = self.processar_apolice(path_b)
        comparativo = self.comparator.comparar(apolice_a, apolice_b)
        parecer = self.reporter.gerar_parecer(comparativo)
        return {
            "apolice_a": apolice_a,
            "apolice_b": apolice_b,
            "meta_a": meta_a,
            "meta_b": meta_b,
            "comparativo": comparativo,
            "parecer": parecer
        }
