
"""AGENTE 4 - O Auditor - Comparador com RAG"""
from core.schemas import ApoliceDOEstruturada, ComparativoItem, RelatorioComparativo
from typing import Tuple

class ComparatorAgent:
    """Armazenamento, Consulta e Comparação - Fluxos 4,5,6 - Uso de RAG SUSEP 541"""
    
    def __init__(self):
        self.susep_rules = {
            "custos_defesa": "Circular SUSEP 541 Art. 12 - Custos de defesa podem ser dentro ou além do LMG",
            "retroatividade": "Base reclamação exige data de retroatividade definida",
            "side_a": "Side A é essencial para proteção pessoal do administrador"
        }
    
    def comparar(self, a: ApoliceDOEstruturada, b: ApoliceDOEstruturada) -> RelatorioComparativo:
        itens = []
        
        # LMG
        itens.append(ComparativoItem(
            campo="LMG - Limite Máximo de Garantia",
            apolice_a=f"R$ {a.lmg:,.0f}" if a.lmg else "Não informado",
            apolice_b=f"R$ {b.lmg:,.0f}" if b.lmg else "Não informado",
            diferenca_critica=(a.lmg or 0) != (b.lmg or 0),
            analise_risco="Diferença de limite impacta diretamente capacidade de indenização. Verificar se suficiente para market cap."
        ))
        
        # Custos Defesa
        itens.append(ComparativoItem(
            campo="Custos de Defesa",
            apolice_a="Além do LMG" if a.cobertura.custos_defesa_alem_lmg else "Dentro do LMG",
            apolice_b="Além do LMG" if b.cobertura.custos_defesa_alem_lmg else "Dentro do LMG",
            diferenca_critica=a.cobertura.custos_defesa_alem_lmg != b.cobertura.custos_defesa_alem_lmg,
            analise_risco="Custos dentro do LMG consomem limite. Risco de esgotamento em litígios longos. Recomendado além do LMG."
        ))
        
        # Side A
        itens.append(ComparativoItem(
            campo="Cobertura Side A (Proteção Pessoal)",
            apolice_a="Sim" if a.cobertura.side_a else "Não / Não claro",
            apolice_b="Sim" if b.cobertura.side_b else "Não / Não claro",
            diferenca_critica=a.cobertura.side_a != b.cobertura.side_a,
            analise_risco="Side A é a proteção última do administrador quando empresa não pode indenizar. Lacuna crítica."
        ))
        
        # Exclusões
        itens.append(ComparativoItem(
            campo="Exclusões Críticas",
            apolice_a=", ".join(a.exclusoes) or "Não identificadas",
            apolice_b=", ".join(b.exclusoes) or "Não identificadas",
            diferenca_critica=set(a.exclusoes) != set(b.exclusoes),
            analise_risco="Verificar exclusão de ato doloso com trânsito em julgado - melhor prática protege até decisão final."
        ))
        
        score_a = 0.8 if a.cobertura.custos_defesa_alem_lmg and a.cobertura.side_a else 0.5
        score_b = 0.8 if b.cobertura.custos_defesa_alem_lmg and b.cobertura.side_a else 0.5
        
        recomendacao = "Apólice A superior" if score_a > score_b else "Apólice B superior" if score_b > score_a else "Equivalentes - decidir por prêmio e franquia"
        
        return RelatorioComparativo(
            itens=itens,
            score_exposicao_oculta_a=1-score_a,
            score_exposicao_oculta_b=1-score_b,
            recomendacao=recomendacao
        )
