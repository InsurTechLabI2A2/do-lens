
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date

class Citacao(BaseModel):
    pagina: int
    trecho_literal: str = Field(description="Trecho exato que comprova a extração")

class Franquia(BaseModel):
    valor: Optional[float] = None
    tipo: Literal["por reclamacao", "anual", "inexistente"] = "por reclamacao"
    citacao: Optional[Citacao] = None

class Cobertura(BaseModel):
    side_a: bool = False
    side_b: bool = False
    side_c: bool = False
    custos_defesa_alem_lmg: Optional[bool] = None
    custos_defesa_citacao: Optional[Citacao] = None

class Temporal(BaseModel):
    vigencia_inicio: Optional[date] = None
    vigencia_fim: Optional[date] = None
    retroatividade: Optional[date] = None
    prazo_complementar_meses: Optional[int] = None
    prazo_suplementar_meses: Optional[int] = None

class ApoliceDOEstruturada(BaseModel):
    """Schema Ontológico D&O - Baseado em Circular SUSEP 541/2016"""
    seguradora: Optional[str] = None
    numero_apolice: Optional[str] = None
    lmg: Optional[float] = Field(None, description="Limite Máximo de Garantia")
    lmg_citacao: Optional[Citacao] = None
    sublimites: dict = Field(default_factory=dict, description="Ex: side_a: 5000000")
    franquia: Franquia = Field(default_factory=Franquia)
    cobertura: Cobertura = Field(default_factory=Cobertura)
    temporal: Temporal = Field(default_factory=Temporal)
    definicoes: dict = Field(default_factory=dict)
    exclusoes: List[str] = Field(default_factory=list)
    extensoes: List[str] = Field(default_factory=list)
    premio: Optional[float] = None
    score_completude: float = Field(0.0, description="0-1 indica confiança da extração")
    observacoes_auditoria: List[str] = Field(default_factory=list)

class ComparativoItem(BaseModel):
    campo: str
    apolice_a: Optional[str]
    apolice_b: Optional[str]
    diferenca_critica: bool
    analise_risco: str

class RelatorioComparativo(BaseModel):
    itens: List[ComparativoItem]
    score_exposicao_oculta_a: float
    score_exposicao_oculta_b: float
    recomendacao: str
