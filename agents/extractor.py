
"""AGENTE 2 - O Escavador - Extrator Jurídico com IA Generativa"""
from core.schemas import ApoliceDOEstruturada, Citacao, Franquia, Cobertura, Temporal
import json, re
from datetime import datetime

# Prompt base - em produção usaria OpenAI function calling
SYSTEM_PROMPT = """
Você é um especialista em seguros D&O e na Circular SUSEP 541/2016.
Extraia EXCLUSIVAMENTE informações presentes no texto.
Se não encontrar, retorne null. NUNCA invente.
Para cada campo, retorne a citação com página e trecho literal.
Formato JSON deve seguir o schema ApoliceDOEstruturada.
"""

class ExtractorAgent:
    """Extração automática - Fluxo 2 - Uso de LLM Generativo"""
    
    def __init__(self, llm_model="gpt-4o-mini", use_mock=True):
        self.llm_model = llm_model
        self.use_mock = use_mock  # Para MVP sem custo de API, usa regex + regras
    
    def extrair(self, texto_bruto: str, metadados: dict) -> ApoliceDOEstruturada:
        if self.use_mock:
            return self._extrair_mock(texto_bruto, metadados)
        else:
            return self._extrair_llm(texto_bruto, metadados)
    
    def _extrair_mock(self, texto: str, meta: dict) -> ApoliceDOEstruturada:
        """MVP didático sem API - simula extração com regex para demonstrar pipeline"""
        lmg = None
        m = re.search(r"LMG.*?R\$\s*([\d\.]+)", texto, re.IGNORECASE)
        if m:
            try:
                lmg = float(m.group(1).replace(".", "").replace(",", "."))
            except:
                lmg = 10000000
        
        side_a = "SIDE A" in texto.upper()
        side_b = "SIDE B" in texto.upper()
        side_c = "SIDE C" in texto.upper()
        custos_alem = "ALEM DO LMG" in texto.upper() or "ALÉM DO LMG" in texto.upper()
        
        exclusoes = []
        if "DOLO" in texto.upper(): exclusoes.append("Ato doloso/fraudulento")
        if "LUCRO" in texto.upper(): exclusoes.append("Lucro indevido")
        
        return ApoliceDOEstruturada(
            seguradora="Seguradora Exemplo - Dados Públicos SUSEP",
            lmg=lmg or 10000000,
            lmg_citacao=Citacao(pagina=1, trecho_literal=texto[:200]),
            cobertura=Cobertura(side_a=side_a, side_b=side_b, side_c=side_c, custos_defesa_alem_lmg=custos_alem),
            exclusoes=exclusoes,
            extensoes=["Multas e Penalidades" if "MULTA" in texto.upper() else "Novas Subsidiárias"],
            score_completude=0.82,
            observacoes_auditoria=["Extração mock para MVP - em produção usar LLM com structured output"]
        )
    
    def _extrair_llm(self, texto: str, meta: dict) -> ApoliceDOEstruturada:
        # Implementação real com OpenAI - mantida como template para evolução
        from openai import OpenAI
        import os
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # ... chamada com response_format json_schema ...
        raise NotImplementedError("Implementar chamada LLM em produção")
