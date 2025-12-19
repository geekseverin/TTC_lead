"""
Interface Streamlit principale du chatbot OTR
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le chemin parent pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from agentAI.chatbot import OTRChatbot
from scripts.config import Config
from components.chat_interface import (
    render_chat_message,
    render_chat_history,
    render_typing_indicator,
    render_source_chips,
    render_response_time,
    render_chat_input
)
from components.document_viewer import render_document_sidebar, render_documents_page
from components.stats_dashboard import render_full_dashboard, render_stats_sidebar

# Configuration de la page
st.set_page_config(
    page_title="OTR Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation du chatbot dans session_state
@st.cache_resource
def initialize_chatbot():
    """Initialise le chatbot (une seule fois)"""
    return OTRChatbot()

# Initialiser les variables de session
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chatbot' not in st.session_state:
    with st.spinner("🚀 Initialisation du chatbot OTR..."):
        st.session_state.chatbot = initialize_chatbot()

if 'page' not in st.session_state:
    st.session_state.page = 'chat'

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/667eea/ffffff?text=OTR", use_container_width=True)
    st.title("🤖 OTR Chatbot")
    st.markdown("Assistant intelligent pour l'Organisation Togolaise des Receveurs")
    
    st.markdown("---")
    
    # Navigation
    st.markdown("## 📱 Navigation")
    
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.page = 'chat'
    
    if st.button("📚 Documents", use_container_width=True):
        st.session_state.page = 'documents'
    
    if st.button("📊 Statistiques", use_container_width=True):
        st.session_state.page = 'stats'
    
    # Afficher les stats dans la sidebar
    render_stats_sidebar()
    
    # Afficher les documents dans la sidebar
    render_document_sidebar()
    
    st.markdown("---")
    
    # Actions
    st.markdown("## ⚙️ Actions")
    
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chatbot.clear_memory()
        st.success("Conversation effacée!")
        st.rerun()
    
    if st.button("🔄 Recharger le chatbot", use_container_width=True):
        st.cache_resource.clear()
        st.session_state.chatbot = initialize_chatbot()
        st.success("Chatbot rechargé!")
        st.rerun()

# Contenu principal selon la page sélectionnée
if st.session_state.page == 'chat':
    # PAGE CHAT
    st.title("💬 Chat avec l'assistant OTR")
    st.markdown("Posez vos questions sur les documents de l'Organisation Togolaise des Receveurs")
    
    # Zone de chat
    chat_container = st.container()
    
    with chat_container:
        # Afficher l'historique
        if st.session_state.messages:
            render_chat_history(st.session_state.messages)
        else:
            st.info("👋 Bonjour! Je suis l'assistant OTR. Posez-moi une question sur les documents disponibles.")
    
    # Zone de saisie (en bas)
    st.markdown("---")
    
    # Input avec suggestions
    user_input = render_chat_input()
    
    if user_input:
        # Ajouter le message utilisateur
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        
        # Afficher immédiatement le message utilisateur
        with chat_container:
            render_chat_message('user', user_input, timestamp)
            render_typing_indicator()
        
        # Obtenir la réponse du chatbot
        response = st.session_state.chatbot.ask(user_input)
        
        # Ajouter la réponse à l'historique
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response['answer'],
            'timestamp': timestamp,
            'sources': response['sources'],
            'from_cache': response['from_cache'],
            'response_time': response['response_time']
        })
        
        # Recharger pour afficher la réponse
        st.rerun()
    
    # Afficher les sources et le temps de réponse pour le dernier message
    if st.session_state.messages and st.session_state.messages[-1]['role'] == 'assistant':
        last_msg = st.session_state.messages[-1]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if 'sources' in last_msg and last_msg['sources']:
                render_source_chips(last_msg['sources'])
        
        with col2:
            if 'response_time' in last_msg:
                render_response_time(
                    last_msg['response_time'],
                    last_msg.get('from_cache', False)
                )

elif st.session_state.page == 'documents':
    # PAGE DOCUMENTS
    render_documents_page()

elif st.session_state.page == 'stats':
    # PAGE STATISTIQUES
    render_full_dashboard()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.85em;'>
    🤖 OTR Chatbot v1.0 | Propulsé par LangChain & OpenRouter | 
    <a href='https://github.com' target='_blank' style='color: #667eea;'>Documentation</a>
</div>
""", unsafe_allow_html=True)