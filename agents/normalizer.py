
"""AGENTE 3 - O Cartógrafo - Normalizador"""
from core.schemas import ApoliceDOEstruturada
import re

class NormalizerAgent:
    """Organização das informações - Fluxo 3"""
    def normalizar(self, apolice: ApoliceDOEstruturada) -> ApoliceDOEstruturada:
        # Normalização de valores - ex: R$ 10MM -> 10000000
        if apolice.lmg and apolice.lmg < 1000:
            apolice.lmg *= 1000000  # Corrige MM
        
        # Padronização de exclusões
        exclusoes_map = {
            "dolo": "Ato doloso/fraudulento",
            "lucro": "Lucro ou vantagem indevida",
            "reclamacao anterior": "Reclamações anteriores à retroatividade"
        }
        norm_excl = []
        for ex in apolice.exclusoes:
            low = ex.lower()
            for k,v in exclusoes_map.items():
                if k in low:
                    norm_excl.append(v)
                    break
            else:
                norm_excl.append(ex)
        apolice.exclusoes = list(set(norm_excl))
        
        # Score de completude recalculado
        campos = [apolice.lmg, apolice.cobertura.side_a, apolice.temporal.retroatividade]
        apolice.score_completude = sum(1 for c in campos if c) / len(campos)
        
        return apolice
