# D\&O Lens \- InsurTechLab | I2A2 Projeto Final

**Plataforma Inteligente para Análise e Comparação de Apólices D\&O**   
**Arquitetura Híbrida Multi-Agente Orquestrada**

> Uma solução simples, porém tecnicamente consistente, possui maior valor didático do que uma arquitetura extremamente complexa.

## 📋 Descrição do Projeto

O **D\&O Lens** automatiza a análise de apólices de seguro Directors and Officers, extraindo, organizando e comparando informações críticas como LMG, Side A/B/C, custos de defesa, retroatividade e exclusões. Utiliza 5 agentes especializados orquestrados via LangGraph.

**Problema:** Comparar apólices D\&O exige horas de especialista em juridiquês e risco. **Solução:** Copiloto de Subscrição e Auditoria com RAG na Circular SUSEP 541/2016.

## 🏗️ Arquitetura \- 5 Agentes

- **Agente 1 \- Porteiro (Ingestor & OCR):** Recebimento PDF/Imagem \- Pypdf \+ Azure Document Intelligence  
- **Agente 2 \- Escavador (Extractor):** Extração com IA Generativa \- LLM Structured Output \+ Citações  
- **Agente 3 \- Cartógrafo (Normalizer):** Organização e Normalização Pydantic  
- **Agente 4 \- Auditor (Comparator):** Armazenamento SQLite \+ ChromaDB \+ RAG SUSEP \+ Comparação \+ Score Exposição Oculta  
- **Agente 5 \- Relator (Reporter):** Apresentação \- Streamlit \+ Mapa de Calor \+ Parecer Técnico

**7 Fluxos do Edital Atendidos:** Recebimento, Extração, Organização, Armazenamento, Consulta, Comparação, Apresentação.

## 🚀 Instalação

git clone https\://github.com/InsurTechLab/do-lens.git

cd do-lens

python \-m venv venv

source venv/bin/activate  \# Windows: venv\\Scripts\\activate

pip install \-r requirements.txt

cp .env.example .env  \# Adicione OPENAI\_API\_KEY se for usar LLM real

## ▶️ Execução

streamlit run app.py

\# Acesse http\://localhost:8501

\# Upload 2 PDFs de exemplo em /data/exemplos/

**Modo Mock (sem API):** O MVP funciona sem chave OpenAI, usando regex para demonstrar pipeline completo.

**Modo Produção (com LLM):** Em `agents/extractor.py` definir `use_mock=False` e configurar `OPENAI_API_KEY`.

## 🧪 Tecnologias Utilizadas

- Python 3.11  
- OCR: Pypdf, Azure Document Intelligence (recomendado), Tesseract  
- LLMs: OpenAI GPT-4o-mini, Gemini 2.0 Flash (Structured Output)  
- Framework Agentes: LangGraph, LangChain  
- Banco: SQLite \+ ChromaDB (Vetorial)  
- Interface: Streamlit  
- Docs: ReportLab, python-pptx, MoviePy

## 👥 Identificação dos Integrantes

- Edmar Martelato  
- Marisa De Moraes  
- Roberto da Silva Gonçalves  
- Rogério Walmor Cervi   
  Grupo: InsurTechLab \- I2A2² 2026

## 📂 Organização do Repositório

/app.py

/agents/ \-\> 5 agentes especializados

/core/ \-\> schemas Pydantic, config, database

/data/exemplos/ \-\> Apólices públicas fictícias baseadas em modelos SUSEP

/Projeto\_Final\_Artefatos/ \-\> Entregáveis: pptx, mp4, relatório, arquitetura

requirements.txt

README.md

LICENSE (MIT)

## 📊 Fontes de Dados

- Modelos públicos de apólices D\&O \- Berkley, Austral (exemplos fictícios baseados em estrutura real)  
- Circular SUSEP 541/2016 \- Documentos disponibilizados pela SUSEP  
- Cláusulas padrão mercado segurador D\&O

## ⚖️ Licença MIT

MIT License \- Copyright (c) 2026 InsurTechLab \- Ver arquivo LICENSE

## 🔮 Evolução Futura

- Suporte a D\&O para IPO e M\&A  
- Integração com análise de risco de crédito  
- Validação jurídica com advogados parceiros