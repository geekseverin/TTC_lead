"""
Gestion du vector store avec FAISS (rapide et sans compilation)
"""
import sys
from pathlib import Path

# Ajouter le chemin parent
sys.path.append(str(Path(__file__).parent.parent))

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from scripts.config import Config

def get_embeddings():
    """Retourne le modèle d'embeddings (local, gratuit, rapide)"""
    return HuggingFaceEmbeddings(
        model_name=Config.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={
            'normalize_embeddings': True,
            'batch_size': 32
        }
    )

def create_vectorstore(documents):
    """Crée et sauvegarde le vectorstore avec FAISS"""
    print("💾 Création du vectorstore avec FAISS...")
    
    embeddings = get_embeddings()
    
    # Créer le vectorstore avec FAISS
    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    # Sauvegarder le vectorstore
    Config.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(Config.VECTORSTORE_DIR))
    
    print(f"✅ Vectorstore créé avec {len(documents)} chunks")
    return vectorstore

def load_vectorstore():
    """Charge le vectorstore existant"""
    embeddings = get_embeddings()
    
    # Charger depuis le dossier
    vectorstore = FAISS.load_local(
        str(Config.VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore

def search_documents(query, k=None):
    """Recherche rapide dans les documents"""
    if k is None:
        k = Config.RETRIEVAL_K
    
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search_with_score(query, k=k)
    
    return results