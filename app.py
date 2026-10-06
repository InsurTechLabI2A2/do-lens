
import streamlit as st
from pathlib import Path
from agents.orchestrator import DOLensOrchestrator
import tempfile, json

st.set_page_config(page_title="D&O Lens - InsurTechLab", layout="wide", page_icon="🛡️")
st.title("🛡️ D&O Lens - InsurTechLab")
st.subheader("Plataforma Inteligente para Análise e Comparação de Apólices D&O")

st.markdown("""
**I2A2 - Instituto de Inteligência Artificial Aplicada | Projeto Final**
Grupo: Edmar Martelato, Marisa De Moraes, Roberto da Silva Gonçalves, Rogério Walmor Cervi
""")

with st.sidebar:
    st.header("Configuração")
    st.info("MVP com Mock LLM para demonstração sem custo de API. Em produção, ativar OpenAI GPT-4o-mini com structured output.")
    st.markdown("**7 Fluxos do Edital:**\n1. Recebimento\n2. Extração\n3. Organização\n4. Armazenamento\n5. Consulta\n6. Comparação\n7. Apresentação")

col1, col2 = st.columns(2)
with col1:
    file_a = st.file_uploader("📄 Apólice A (PDF)", type=["pdf"], key="a")
with col2:
    file_b = st.file_uploader("📄 Apólice B (PDF)", type=["pdf"], key="b")

if file_a and file_b:
    with tempfile.TemporaryDirectory() as tmp:
        path_a = Path(tmp) / "apolice_a.pdf"
        path_b = Path(tmp) / "apolice_b.pdf"
        path_a.write_bytes(file_a.read())
        path_b.write_bytes(file_b.read())
        
        if st.button("🔍 Analisar e Comparar - Executar 5 Agentes", type="primary"):
            orchestrator = DOLensOrchestrator()
            with st.spinner("Agentes em ação: Ingestor -> Escavador -> Cartógrafo -> Auditor -> Relator..."):
                resultado = orchestrator.comparar_apolices(path_a, path_b)
            
            st.success("Processamento concluído!")
            
            # Abas
            tab1, tab2, tab3 = st.tabs(["📊 Mapa de Calor", "📑 JSON Estruturado", "📝 Parecer Técnico"])
            
            with tab1:
                st.subheader("Mapa de Calor de Cobertura")
                for item in resultado["comparativo"].itens:
                    cor = "🔴" if item.diferenca_critica else "🟢"
                    with st.expander(f"{cor} {item.campo}"):
                        c1, c2 = st.columns(2)
                        c1.metric("Apólice A", item.apolice_a)
                        c2.metric("Apólice B", item.apolice_b)
                        st.warning(f"Análise de Risco: {item.analise_risco}")
                
                st.metric("Score Exposição Oculta A", f"{resultado['comparativo'].score_exposicao_oculta_a:.0%}")
                st.metric("Score Exposição Oculta B", f"{resultado['comparativo'].score_exposicao_oculta_b:.0%}")
                st.info(f"**Recomendação:** {resultado['comparativo'].recomendacao}")
            
            with tab2:
                st.json(resultado["apolice_a"].model_dump(mode="json"))
                st.json(resultado["apolice_b"].model_dump(mode="json"))
            
            with tab3:
                st.markdown(resultado["parecer"])
                st.download_button("Baixar Parecer", resultado["parecer"], file_name="parecer_do_lens.md")
else:
    st.info("Faça upload de 2 apólices em PDF para iniciar. Use os exemplos em /data/exemplos/")
    
    st.subheader("💡 Chat Jurídico - Consulta RAG (Demonstração)")
    pergunta = st.text_input("Pergunte: Ex: Qual apólice cobre multas da CVM além do LMG?")
    if pergunta:
        st.write(f"**Resposta simulada com RAG SUSEP 541:** Baseado nas apólices carregadas, a cobertura de multas e penalidades é uma extensão típica de D&O. Verificar cláusula de Extensões e definição de Perda. Recomenda-se análise da Circular SUSEP 541 Art. 8.")
