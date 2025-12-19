"""
Composant de visualisation des documents
"""
import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.config import Config

def count_documents():
    """Compte tous les documents disponibles"""
    docs_path = Config.DOCUMENTS_DIR
    
    if not docs_path.exists():
        return 0, {}
    
    # Compter par extension
    counts = {}
    total = 0
    
    for file in docs_path.rglob("*"):
        if file.is_file() and not file.name.startswith('.'):
            ext = file.suffix.lower()
            counts[ext] = counts.get(ext, 0) + 1
            total += 1
    
    return total, counts

def list_all_documents():
    """Liste tous les documents avec leurs métadonnées"""
    docs_path = Config.DOCUMENTS_DIR
    documents = []
    
    if not docs_path.exists():
        return documents
    
    for file in docs_path.rglob("*"):
        if file.is_file() and not file.name.startswith('.'):
            documents.append({
                'name': file.name,
                'path': str(file.relative_to(docs_path)),
                'size': file.stat().st_size,
                'extension': file.suffix.lower(),
                'modified': file.stat().st_mtime
            })
    
    # Trier par nom
    documents.sort(key=lambda x: x['name'])
    return documents

def format_size(size_bytes):
    """Formate la taille en format lisible"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def get_file_emoji(extension):
    """Retourne un emoji selon l'extension"""
    emoji_map = {
        '.pdf': '📄',
        '.docx': '📝',
        '.doc': '📝',
        '.xlsx': '📊',
        '.xls': '📊',
        '.txt': '📃',
        '.pptx': '📊',
        '.ppt': '📊',
        '.csv': '📈',
    }
    return emoji_map.get(extension, '📄')

def render_document_sidebar():
    """Affiche la sidebar avec la liste des documents"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📚 Base de connaissances OTR")
    
    # Statistiques
    total, counts = count_documents()
    
    st.sidebar.metric("📁 Documents disponibles", total)
    
    if total == 0:
        st.sidebar.warning("Aucun document trouvé. Ajoutez des documents dans le dossier `data/documents/`")
        return
    
    # Répartition par type
    with st.sidebar.expander("📊 Répartition par type", expanded=False):
        for ext, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            emoji = get_file_emoji(ext)
            st.write(f"{emoji} **{ext[1:].upper()}**: {count}")
    
    # Liste des documents
    with st.sidebar.expander("📑 Liste des documents", expanded=False):
        documents = list_all_documents()
        
        # Recherche
        search = st.text_input("🔍 Rechercher un document", "")
        
        if search:
            documents = [d for d in documents if search.lower() in d['name'].lower()]
        
        # Afficher les documents
        for doc in documents:
            emoji = get_file_emoji(doc['extension'])
            st.markdown(f"""
            <div style='background-color: #f8f9fa; 
                        padding: 8px; 
                        border-radius: 8px; 
                        margin: 5px 0;
                        border-left: 3px solid #667eea;'>
                {emoji} **{doc['name']}**<br>
                <small style='color: #6b7280;'>{format_size(doc['size'])}</small>
            </div>
            """, unsafe_allow_html=True)

def render_documents_page():
    """Affiche une page complète de gestion des documents"""
    st.title("📚 Gestion des documents OTR")
    
    # Statistiques globales
    total, counts = count_documents()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total documents", total)
    with col2:
        st.metric("Types de fichiers", len(counts))
    with col3:
        total_size = sum(f.stat().st_size for f in Config.DOCUMENTS_DIR.rglob("*") if f.is_file())
        st.metric("Taille totale", format_size(total_size))
    
    st.markdown("---")
    
    # Liste détaillée
    st.subheader("📋 Liste détaillée des documents")
    
    documents = list_all_documents()
    
    if not documents:
        st.info("Aucun document trouvé. Ajoutez des fichiers PDF, Word, Excel ou texte dans le dossier `data/documents/`")
        return
    
    # Tableau des documents
    for doc in documents:
        with st.expander(f"{get_file_emoji(doc['extension'])} {doc['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Type:** {doc['extension'][1:].upper()}")
                st.write(f"**Taille:** {format_size(doc['size'])}")
            with col2:
                st.write(f"**Chemin:** `{doc['path']}`")
                from datetime import datetime
                modified = datetime.fromtimestamp(doc['modified'])
                st.write(f"**Modifié:** {modified.strftime('%d/%m/%Y %H:%M')}")