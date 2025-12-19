"""
Composant d'interface de chat réutilisable
"""
import streamlit as st
from datetime import datetime

def render_chat_message(role, content, timestamp=None):
    """
    Affiche un message de chat avec un style moderne
    
    Args:
        role: 'user' ou 'assistant'
        content: Le contenu du message
        timestamp: Horodatage optionnel
    """
    if role == "user":
        col1, col2 = st.columns([1, 5])
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 15px; 
                        border-radius: 15px; 
                        margin: 10px 0;
                        color: white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <strong>👤 Vous</strong><br>
                <div style='margin-top: 8px;'>{content}</div>
                {f"<small style='opacity: 0.8;'>{timestamp}</small>" if timestamp else ""}
            </div>
            """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                        padding: 15px; 
                        border-radius: 15px; 
                        margin: 10px 0;
                        color: #2d3748;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <strong>🤖 Assistant OTR</strong><br>
                <div style='margin-top: 8px;'>{content}</div>
                {f"<small style='opacity: 0.7;'>{timestamp}</small>" if timestamp else ""}
            </div>
            """, unsafe_allow_html=True)

def render_chat_history(messages):
    """
    Affiche tout l'historique de chat
    
    Args:
        messages: Liste de dictionnaires avec 'role', 'content', et optionnellement 'timestamp'
    """
    for msg in messages:
        timestamp = msg.get('timestamp', None)
        render_chat_message(msg['role'], msg['content'], timestamp)

def render_typing_indicator():
    """Affiche un indicateur de saisie"""
    st.markdown("""
    <div style='padding: 10px; margin: 10px 0;'>
        <span style='color: #667eea;'>● ● ●</span> <em>Assistant OTR réfléchit...</em>
    </div>
    """, unsafe_allow_html=True)

def render_source_chips(sources):
    """
    Affiche les sources sous forme de chips élégants
    
    Args:
        sources: Liste de dictionnaires de métadonnées de sources
    """
    if not sources:
        return
    
    st.markdown("**📚 Sources consultées:**")
    
    # Créer des chips pour chaque source unique
    unique_sources = {}
    for source in sources:
        filename = source.get('filename', 'Document inconnu')
        if filename not in unique_sources:
            unique_sources[filename] = source
    
    # Afficher en colonnes
    cols = st.columns(min(len(unique_sources), 3))
    for idx, (filename, metadata) in enumerate(unique_sources.items()):
        with cols[idx % 3]:
            file_type = metadata.get('file_type', 'doc')
            emoji = {
                'pdf': '📄',
                'docx': '📝',
                'xlsx': '📊',
                'txt': '📃',
                'pptx': '📊'
            }.get(file_type, '📄')
            
            st.markdown(f"""
            <div style='background-color: #f0f2f6; 
                        padding: 8px 12px; 
                        border-radius: 20px; 
                        margin: 5px 0;
                        display: inline-block;
                        font-size: 0.9em;'>
                {emoji} {filename}
            </div>
            """, unsafe_allow_html=True)

def render_response_time(response_time, from_cache=False):
    """Affiche le temps de réponse"""
    if from_cache:
        st.markdown(f"""
        <div style='text-align: right; color: #10b981; font-size: 0.85em; margin-top: 5px;'>
            ⚡ Réponse instantanée (cache)
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align: right; color: #6b7280; font-size: 0.85em; margin-top: 5px;'>
            ⏱️ {response_time:.2f}s
        </div>
        """, unsafe_allow_html=True)

def render_chat_input():
    """Rendu d'un input de chat stylisé avec suggestions"""
    
    # Suggestions de questions
    st.markdown("**💡 Questions suggérées:**")
    suggestions = [
        "Qu'est-ce que l'OTR ?",
        "Quels sont les services proposés ?",
        "Comment contacter l'OTR ?",
        "Quelle est la mission de l'OTR ?"
    ]
    
    cols = st.columns(2)
    for idx, suggestion in enumerate(suggestions):
        with cols[idx % 2]:
            if st.button(suggestion, key=f"suggestion_{idx}", use_container_width=True):
                return suggestion
    
    # Input principal
    return st.chat_input("Posez votre question sur l'OTR...")