#!/usr/bin/env python3
"""
app.py - Interface web Streamlit para o sistema RAG com citação.

Esta interface permite:
1. Upload de documentos (PDF, TXT, MD)
2. Ingestão e indexação dos documentos
3. Busca semântica de documentos
4. Geração de respostas com citações de fontes

Fluxo:
1. Uploader documentos → Ingestão (botão "Indexar")
2. Campo de busca → Pesquisa no índice FAISS
3. Resultado da busca → Geração de resposta com citações
"""

import streamlit as st
import os
import tempfile
import json
from pathlib import Path

# Import our RAG scripts
from ingest import ingest_documents, create_embeddings, build_faiss_index, save_index
from search import search
from generate import generate_response, load_metadata


# Page configuration
st.set_page_config(
    page_title="RAG System with Citations",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================
# CUSTOM CSS - Heavy Visual Upgrade with Emojis
# ============================================
st.markdown("""
<style>
    /* ==========================================
       3D CSS VARIABLES - Tema escuro premium
       ========================================== */
    :root {
        --bg-primary: #0a0a1a;
        --bg-secondary: #12122a;
        --bg-card: #1a1a3a;
        --bg-card-hover: #22224a;
        --fg-primary: #e0e0f0;
        --fg-secondary: #a0a0c0;
        --fg-muted: #6a6a8a;
        --accent: #00d4aa;
        --accent-secondary: #6c5ce7;
        --accent-tertiary: #ff6b6b;
        --border: #2a2a4a;
        --gradient-start: #0f0f23;
        --gradient-end: #1a1a3a;
        --card-gradient: linear-gradient(135deg, #1e1e3f 0%, #2d2d5a 100%);
        --shadow-soft: 0 8px 32px rgba(0, 0, 0, 0.5);
        --shadow-glow: 0 0 40px rgba(0, 212, 170, 0.3);
        --shadow-inset: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    /* ==========================================
       BACKGROUND - Degradê 3D escuro com movimento
       ========================================== */
    .main {
        padding: 3rem 2rem;
        background:
            radial-gradient(at top left, var(--accent) 0%, transparent 50%),
            radial-gradient(at bottom right, var(--accent-secondary) 0%, transparent 50%),
            linear-gradient(180deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }

    /* Camada de fundo 3D animada */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        background-image:
            radial-gradient(circle at 20% 20%, rgba(0, 212, 170, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(108, 92, 231, 0.06) 0%, transparent 50%);
        animation: float-bg 25s ease-in-out infinite;
    }

    .main::after {
        content: '';
        position: fixed;
        bottom: -50%;
        right: -50%;
        width: 400%;
        height: 400%;
        background:
            conic-gradient(from 0deg, var(--accent), var(--accent-secondary), #ff6b6b, var(--accent), 360deg),
            radial-gradient(circle at center, rgba(0, 212, 170, 0.03) 0%, transparent 50%);
        z-index: 0;
        animation: spin 20s linear infinite;
        opacity: 0.3;
    }

    @keyframes float-bg {
        0%, 100% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, 30px) scale(1.02); }
        66% { transform: translate(-20px, -20px) scale(0.98); }
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Gradient glow orbit */
    .main .glow-orbit {
        position: fixed;
        width: 600px;
        height: 600px;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.4;
        animation: orbit 30s linear infinite;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes orbit {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    /* ==========================================
       CONTAINERS E CARDs 3D
       ========================================== */
    .main > div {
        position: relative;
        z-index: 1;
        gap: 2rem;
    }

    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-soft), 0 0 0 1px rgba(255, 255, 255, 0.02);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }

    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .card:hover::before {
        opacity: 1;
    }

    .card:hover {
        border-color: var(--accent);
        box-shadow: var(--shadow-glow), 0 12px 40px rgba(0, 0, 0, 0.5), 0 0 20px var(--accent-glow);
        transform: translateY(-4px) scale(1.01);
    }

    .card:active {
        transform: translateY(-1px) scale(1.005);
    }

    .card .tag {
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 0.65rem;
        padding: 0.2rem 0.6rem;
        background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
        color: white;
        border-radius: 20px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ==========================================
       BUTTONS - Vibrant hover com efeito 3D
       ========================================== */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 1.75rem;
        font-weight: 600;
        font-size: 1.05rem;
        cursor: pointer;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0, 212, 170, 0.4);
        position: relative;
        overflow: hidden;
        width: 100%;
        margin: 0.5rem 0;
        z-index: 1;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.03) !important;
        box-shadow: 0 8px 30px var(--accent-glow), 0 0 30px var(--accent), 0 0px 0 1px rgba(0, 212, 170, 0.1) !important;
        background: linear-gradient(135deg, #00f5c4 0%, #a084ff 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(1px) scale(0.98);
        box-shadow: 0 2px 10px rgba(0, 212, 170, 0.3) !important;
    }

    .stButton > button:focus-visible {
        outline: 2px solid #fff;
        outline-offset: 3px;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6c5ce7 0%, #00d4aa 100%);
        box-shadow: 0 4px 20px rgba(108, 92, 231, 0.4);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #a084ff 0%, #6c5ce7 100%) !important;
        box-shadow: 0 8px 30px rgba(160, 132, 255, 0.4) !important;
    }

    .stButton > button[kind="secondary"] {
        background: var(--bg-card);
        color: var(--fg-primary);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.85rem 1.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button[kind="secondary"]:hover {
        background: var(--bg-secondary);
        border-color: var(--accent);
        color: var(--accent);
        box-shadow: 0 4px 20px var(--accent-glow);
    }

    .stButton > button[kind="danger"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
    }

    .stButton > button[kind="danger"]:hover {
        background: linear-gradient(135deg, #ff8c42 0%, #ff6b6b 100%);
        box-shadow: 0 4px 20px rgba(255, 107, 107, 0.4);
    }

    /* ==========================================
       INPUTS E TEXT INPUTS COM BORDA GLOW
       ========================================== */
    .stTextInput > div > div > input {
        background: var(--bg-card);
        border: 2px solid var(--border);
        border-radius: 16px;
        color: var(--fg-primary);
        padding: 0.875rem 1.25rem;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        outline: none;
        width: 100%;
    }

    .stTextInput > div > div > input::placeholder {
        color: var(--fg-muted);
        opacity: 0.7;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 4px var(--accent-glow);
        background: rgba(0, 212, 170, 0.03);
    }

    .stTextInput > div > div > input:focus:invalid {
        box-shadow: 0 0 0 4px rgba(255, 95, 87, 0.2);
    }

    /* ==========================================
       SELECTBOX E RADIO
       ========================================== */
    .stSelect > div > div > div {
        background: var(--bg-card);
        border: 2px solid var(--border);
        border-radius: 16px;
        color: var(--fg-primary);
    }

    .stSelect > div > div > div:focus-within {
        border-color: var(--accent);
        box-shadow: 0 0 0 4px var(--accent-glow);
    }

    /* ==========================================
       RESULTADOS E EXPANDERS ESTILO CHAT
       ========================================== */
    .result-container {
        background: var(--bg-card-hover);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.75rem;
        margin: 1.25rem 0;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .result-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 0%;
        background: linear-gradient(var(--accent), var(--accent-secondary));
        transition: height 0.3s ease;
    }

    .result-container:hover {
        border-color: var(--accent);
        box-shadow: var(--shadow-glow), 0 8px 25px rgba(0, 0, 0, 0.3);
        transform: translateX(4px);
    }

    .result-container:hover::before {
        height: 100%;
    }

    .result-container .score {
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 0.7rem;
        color: var(--fg-muted);
        background: var(--accent-glow);
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-weight: 700;
    }

    /* Estilizar títulos dos expanders com emojis animados */
    .stExpander > summary {
        color: var(--fg-primary);
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin: -1.75rem -1.75rem 0.75rem -1.75rem;
        background: var(--bg-secondary);
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }

    .stExpander > summary:hover {
        background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
        color: white;
        transform: scale(1.02);
    }

    .stExpander > summary:hover span {
        color: white;
    }

    /* Emoji nos títulos dos expanders - maior e mais vibrante */
    .stExpander > summary::before {
        content: "🔍 ";
        color: var(--accent);
        font-size: 1.4rem;
        min-width: 1.4rem;
        text-align: center;
        float: left;
        margin-right: 0.75rem;
        font-weight: 900;
    }

    /* ==========================================
       CITAÇÕES ESTILIZADAS COM ICONES
       ========================================== */
    .citation {
        font-size: 0.85rem;
        color: var(--fg-secondary);
        margin-top: 0.75rem;
        padding: 0.75rem 1rem;
        background: var(--bg-secondary);
        border-radius: 12px;
        border-left: 4px solid var(--accent);
        transition: all 0.3s ease;
        position: relative;
    }

    .citation:hover {
        border-left-color: var(--accent-secondary);
        background: rgba(108, 92, 231, 0.15);
        transform: translateX(4px);
    }

    .citation::before {
        content: "📚 ";
        font-size: 1rem;
        margin-right: 0.5rem;
        vertical-align: middle;
    }

    .citation .source-name {
        color: var(--accent-secondary);
        font-size: 0.75rem;
        margin-left: 0.5rem;
        background: var(--accent-glow);
        padding: 0.1rem 0.4rem;
        border-radius: 6px;
        font-weight: 600;
    }

    /* ==========================================
       STATUS BADGES COM ANIMAÇÃO
       ========================================== */
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 28px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .status-badge::before {
        content: "";
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }

    .status-success {
        background: rgba(0, 212, 170, 0.15);
        color: var(--success);
        border: 1px solid var(--success);
    }

    .status-success::before {
        background: var(--success);
        margin-right: 0.5rem;
    }

    .status-info {
        background: rgba(108, 92, 231, 0.15);
        color: var(--accent-secondary);
        border: 1px solid var(--accent-secondary);
    }

    .status-info::before {
        background: var(--accent-secondary);
        margin-right: 0.5rem;
    }

    .status-warning {
        background: rgba(247, 183, 49, 0.15);
        color: var(--warning);
        border: 1px solid var(--warning);
    }

    .status-warning::before {
        background: var(--warning);
        margin-right: 0.5rem;
    }

    .status-error {
        background: rgba(255, 95, 87, 0.15);
        color: var(--error);
        border: 1px solid var(--error);
    }

    .status-error::before {
        background: var(--error);
        margin-right: 0.5rem;
    }

    /* Tag chip aprimorado */
    .tag-chip {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
        color: white;
        border-radius: 24px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0.3rem 0.2rem;
        box-shadow: 0 2px 8px rgba(0, 212, 170, 0.3);
        transition: all 0.3s ease;
    }

    .tag-chip:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 4px 15px var(--accent-glow);
    }

    /* ==========================================
       SIDEBAR - Logo 3D ANIMADA COMPLETA
       ========================================== */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        border-right: 1px solid var(--border);
    }

    .sidebar-logo {
        text-align: center;
        padding: 2rem 1rem 1.5rem 1rem;
        margin: -1rem -1rem 2rem -1rem;
    }

    .sidebar-logo .logo-3d-card {
        width: 100px;
        height: 100px;
        background: var(--card-gradient);
        border: 3px solid var(--accent);
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        box-shadow: var(--shadow-soft), 0 0 30px var(--accent-glow);
        position: relative;
        transition: all 0.4s ease;
    }

    .sidebar-logo .logo-3d-card:hover {
        transform: scale(1.1) rotate(10deg);
        box-shadow: var(--shadow-glow), 0 0 50px var(--accent-glow), 0 0 30px rgba(108, 92, 231, 0.5);
        border-color: var(--accent-secondary);
    }

    .sidebar-logo .logo-3d-card .emoji {
        font-size: 3rem;
        filter: drop-shadow(0 0 10px var(--accent-glow));
        transition: all 0.3s ease;
    }

    .sidebar-logo .logo-3d-card:hover .emoji {
        transform: scale(1.2) rotate(15deg);
        filter: drop-shadow(0 0 20px var(--accent-glow)) drop-shadow(0 0 30px var(--accent-secondary));
    }

    .sidebar-logo h3 {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-secondary) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }

    .sidebar-logo p {
        color: var(--fg-muted);
        font-size: 0.85rem;
        letter-spacing: 1px;
    }

    /* Efeito de brilho scan no logo */
    .sidebar-logo .logo-3d-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 212, 170, 0.1), transparent);
        transform: translateX(-100%);
        animation: shine 4s ease-in-out infinite;
    }

    @keyframes shine {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }

    /* ==========================================
       AVATAR E CHAT MESSAGES (se houver chat)
       ========================================== */
    .chat-message {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .chat-message.user {
        background: linear-gradient(135deg, var(--accent), #00ffcc);
        color: #0a0a20;
    }

    .chat-message.assistant {
        background: var(--bg-card);
        color: var(--fg-primary);
    }

    /* ==========================================
       PROGRESSO E SPINNER
       ========================================== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent), var(--accent-secondary));
    }

    .stSpinner > div {
        border-color: var(--accent) transparent transparent transparent !important;
        border-top-color: transparent !important;
        animation: spin-spinner 0.8s linear infinite !important;
    }

    @keyframes spin-spinner {
        to { transform: rotate(360deg); }
    }

    /* ==========================================
       MENSAGENS DE STATUS
       ========================================== */
    .stSuccess > div {
        background: rgba(0, 212, 170, 0.1);
        border: 1px solid var(--success);
        color: var(--success);
    }

    .stError > div {
        background: rgba(255, 95, 87, 0.1);
        border: 1px solid var(--error);
        color: var(--error);
    }

    .stWarning > div {
        background: rgba(247, 183, 49, 0.1);
        border: 1px solid var(--warning);
        color: var(--warning);
    }

    .stInfo > div {
        background: rgba(108, 92, 231, 0.1);
        border: 1px solid var(--accent-secondary);
        color: var(--accent-secondary);
    }

    /* ==========================================
       COLUNAS E LAYOUT
       ========================================== */
    .stColumns > div {
        gap: 1rem;
    }

    .stExpander {
        border-radius: 16px;
        border: none;
    }

    .stExpander:hover {
        border: 1px solid var(--accent-glow);
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .main {
            padding: 1.5rem 1rem;
        }

        .card {
            padding: 1.5rem;
            margin: 0.75rem 0;
        }

        .sidebar-logo {
            padding: 1rem;
            margin: -0.5rem -0.5rem 1rem -0.5rem;
        }

        .sidebar-logo .logo-3d-card {
            width: 70px;
            height: 70px;
        }

        .sidebar-logo .logo-3d-card .emoji {
            font-size: 2rem;
        }

        .stButton > button {
            padding: 0.7rem 1.2rem;
            font-size: 0.95rem;
        }
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "index_built" not in st.session_state:
        st.session_state.index_built = False
    if "embeddings" not in st.session_state:
        st.session_state.embeddings = None
    if "metadata" not in st.session_state:
        st.session_state.metadata = None
    if "chunks" not in st.session_state:
        st.session_state.chunks = None
    if "documents_processed" not in st.session_state:
        st.session_state.documents_processed = 0


def sidebar():
    """Render the sidebar with upgraded visual design."""
    st.sidebar.title("🔍 RAG System")

    # Área de logo 3D animada no topo da sidebar
    st.markdown("""
    <div class="sidebar-logo">
        <div class="logo-3d-card">
            <span class="emoji" style="font-size: 3rem;">🔍</span>
        </div>
        <h3>RAG Inteligente</h3>
        <p>Busca Semântica</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    st.sidebar.subheader("📁 Documentos")
    docs_dir = st.sidebar.text_input("Pasta de documentos", value="docs")

    st.sidebar.subheader("⚙️ Configurações de Indexação")
    chunk_size = st.sidebar.slider("Tamanho do chunk", 100, 1000, 500, 50, label_visibility="collapsed")
    chunk_overlap = st.sidebar.slider("Sobreposição do chunk", 0, 200, 50, 10, label_visibility="collapsed")

    st.sidebar.markdown("---")

    # Botão com animação de hover - agora com emojis ainda mais vibrantes
    if st.sidebar.button("📥 Indexar Documentos", type="primary", disabled=st.session_state.index_built):
        with st.sidebar.spinner("✨ Processando documentos"):
            # Create docs directory if needed
            os.makedirs(docs_dir, exist_ok=True)

            # Ingest documents
            chunks, metadata = ingest_documents(
                docs_dir,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )

            if chunks:
                # Create embeddings
                st.session_state.embeddings = create_embeddings(chunks)

                # Build FAISS index
                index = build_faiss_index(st.session_state.embeddings)

                # Save index and metadata
                save_index(index, st.session_state.embeddings, metadata, "./data")

                st.session_state.index_built = True
                st.session_state.chunks = chunks
                st.session_state.metadata = metadata
                st.session_state.documents_processed = len(metadata)

                st.sidebar.markdown('<span class="status-badge status-success">✅ Concluído</span>', unsafe_allow_html=True)
                st.sidebar.success(f"{len(metadata)} documentos processados! ✅")
            else:
                st.sidebar.markdown('<span class="status-badge status-error">❌ Erro</span>', unsafe_allow_html=True)
                st.sidebar.error("Nenhum documento encontrado na pasta especificada. 📁")

    st.sidebar.markdown("---")

    # Chip de status aprimorado
    if st.session_state.index_built:
        st.sidebar.markdown('<span class="tag-chip">✅ Indexado</span>', unsafe_allow_html=True)

    if st.session_state.get("documents_processed", 0) > 0:
        st.sidebar.markdown(f'<span class="tag-chip">📄 {st.session_state.documents_processed} docs</span>', unsafe_allow_html=True)

    # Nova área de estatísticas visuais
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Estatísticas")

    # Tags de status coloridas
    chips = []
    if st.session_state.index_built:
        chips.append('<span class="tag-chip">✅ Ready</span>')
    else:
        chips.append('<span class="tag-chip">⏳ Pending</span>')

    if st.session_state.get("documents_processed", 0) > 0:
        chips.append(f'<span class="tag-chip">📄 {st.session_state.documents_processed} docs</span>')

    if chips:
        st.sidebar.markdown(" | ".join(chips), unsafe_allow_html=True)

    st.sidebar.markdown("---")

    if st.sidebar.button("🗑️ Reiniciar", type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def main_area():
    """Render the main area with visual upgrades."""
    st.title("📚 Sistema RAG com Citação")
    st.markdown("---")

    # Check if index is built
    if not st.session_state.index_built:
        st.markdown("""
        <div class="card status-info">
            <h4>👈 Bem-vindo!</h4>
            <p>Por favor, indexe documentos usando a barra lateral para começar.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Como usar:**
        1. Adicione documentos (PDF, TXT, MD) na pasta `docs/` ou especifique o caminho
        2. Clique em "Indexar Documentos" na barra lateral
        3. Faça buscas e receba respostas com citações de fontes
        """)
        return

    # Status inicial
    st.markdown("""
    <div class="card status-success">
        <span class="status-badge">✅ Pronto</span>
        <span class="tag-chip">📄 Sistema ativo</span>
    </div>
    """, unsafe_allow_html=True)

    # Search section
    st.subheader("🔎 Buscar em documentos")
    query = st.text_input("Digite sua pergunta", placeholder="Ex: Qual é a política de reembolso?")

    col1, col2 = st.columns([4, 1])
    with col2:
        k = st.number_input("Número de resultados", min_value=1, max_value=10, value=4)

    if st.button("🔍 Buscar", type="primary") and query:
        with st.spinner("Buscando documentos relevantes..."):
            # Perform search
            results, indices, scores = search(query, "./data", k=k)

            st.session_state.search_results = results
            st.session_state.search_scores = scores

    # Display results
    if hasattr(st.session_state, "search_results") and st.session_state.search_results:
        st.markdown("---")
        st.subheader("📋 Resultados da Busca")

        for i, result in enumerate(st.session_state.search_results):
            with st.expander(f"Resultado {i+1} - Similaridade: {st.session_state.search_scores[0][i]:.4f}", expanded=i < 2):
                st.write(f"**Arquivo:** {result.get('source', 'N/A')}")
                st.write(f"**Similaridade:** {result.get('similarity_score', 0):.4f}")
                st.write("**Conteúdo:**")
                st.write(result.get('text', '')[:500] + ("..." if len(result.get('text', '')) > 500 else ""))

                # Citation info with emoji
                if 'chunk_index' in result:
                    st.markdown(f"""
                    <div class="citation">
                        📝 Trecho #{result['chunk_index'] + 1} de {result.get('source', '')}
                    </div>
                    """, unsafe_allow_html=True)

        # Generate response
        st.markdown("---")
        st.subheader("💬 Gerar Resposta com Citação")

        if st.button("🤖 Gerar Resposta", type="primary"):
            with st.spinner("Gerando resposta com citações..."):
                query = st.session_state.get("search_results", [{}])[0] if st.session_state.search_results else {}

                # Generate response
                response, citations = generate_response(
                    query,
                    st.session_state.search_results,
                    st.session_state.metadata,
                    "claude-3-5-sonnet"
                )

                st.markdown("### Resposta:")
                st.write(response)

                st.markdown("### Fontes/Citações:")
                for cite in citations:
                    st.markdown(f"""
                    <div class="citation">
                        🔢 [{cite['id']}]: {cite['source']} (chunk {cite['chunk']})
                    </div>
                    """, unsafe_allow_html=True)

    # If no results yet, show instruction
    if not st.session_state.index_built:
        st.info("Indexe documentos primeiro usando a barra lateral.")


def main():
    """Main entry point for the Streamlit app."""
    init_session_state()
    sidebar()
    main_area()


if __name__ == "__main__":
    main()