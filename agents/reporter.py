
"""AGENTE 5 - O Relator - Apresentação ao usuário"""
from core.schemas import RelatorioComparativo

class ReporterAgent:
    """Apresentação dos resultados - Fluxo 7"""
    def gerar_parecer(self, rel: RelatorioComparativo) -> str:
        parecer = f"""
# PARECER TÉCNICO D&O - InsurTechLab

## Resumo Executivo
{rel.recomendacao}

## Score de Exposição Oculta
- Apólice A: {rel.score_exposicao_oculta_a:.0%} de exposição
- Apólice B: {rel.score_exposicao_oculta_b:.0%} de exposição

## Detalhamento Comparativo
"""
        for item in rel.itens:
            icone = "🔴 CRÍTICA" if item.diferenca_critica else "🟢 OK"
            parecer += f"""
### {item.campo} - {icone}
- A: {item.apolice_a}
- B: {item.apolice_b}
- Análise: {item.analise_risco}
"""
        parecer += "\n---\nGerado por D&O Lens - InsurTechLab - Base SUSEP 541/2016"
        return parecer
