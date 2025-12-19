"""
Script d'ingestion des documents - Version simplifiée et rapide
"""
import sys
from pathlib import Path

# Ajouter le chemin parent pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    TextLoader,
    UnstructuredPowerPointLoader
)
from scripts.config import Config
from scripts.chuncking import chunk_documents
from scripts.storage import create_vectorstore
import time

def get_loader_for_file(file_path):
    """Retourne le bon loader selon l'extension"""
    extension = file_path.suffix.lower()
    
    loaders = {
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
        '.doc': Docx2txtLoader,
        '.xlsx': UnstructuredExcelLoader,
        '.xls': UnstructuredExcelLoader,
        '.txt': TextLoader,
        '.pptx': UnstructuredPowerPointLoader,
        '.ppt': UnstructuredPowerPointLoader,
    }
    
    return loaders.get(extension)

def load_single_document(file_path):
    """Charge un seul document"""
    loader_class = get_loader_for_file(file_path)
    
    if loader_class is None:
        print(f"⚠️  Format non supporté: {file_path.suffix}")
        return None
    
    try:
        loader = loader_class(str(file_path))
        docs = loader.load()
        
        # Ajouter des métadonnées enrichies
        for doc in docs:
            doc.metadata['filename'] = file_path.name
            doc.metadata['file_type'] = file_path.suffix[1:]
            doc.metadata['source_path'] = str(file_path)
        
        return docs
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {file_path.name}: {e}")
        return None

def load_all_documents():
    """Charge tous les documents du dossier"""
    documents_path = Config.DOCUMENTS_DIR
    all_documents = []
    
    print("\n" + "=" * 60)
    print("📂 CHARGEMENT DES DOCUMENTS OTR")
    print("=" * 60)
    print(f"Dossier: {documents_path}\n")
    
    # Extensions supportées
    supported_extensions = {'.pdf', '.docx', '.doc', '.xlsx', '.xls', '.txt', '.pptx', '.ppt'}
    
    # Parcourir tous les fichiers
    files = [f for f in documents_path.rglob("*") if f.suffix.lower() in supported_extensions]
    
    if not files:
        print("⚠️  Aucun document trouvé!")
        print(f"   Ajoutez des fichiers dans: {documents_path}")
        return []
    
    print(f"📁 {len(files)} fichiers trouvés\n")
    
    # Charger chaque fichier
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Chargement: {file_path.name}...", end=" ")
        docs = load_single_document(file_path)
        
        if docs:
            all_documents.extend(docs)
            print(f"✅ ({len(docs)} pages/sections)")
        else:
            print("❌")
    
    print(f"\n✨ Total: {len(all_documents)} documents/pages chargés")
    return all_documents

def ingest_documents():
    """Pipeline complet d'ingestion"""
    start_time = time.time()
    
    print("\n🚀 DÉBUT DE L'INGESTION DES DOCUMENTS OTR\n")
    print("=" * 60)
    
    # 1. Charger les documents
    documents = load_all_documents()
    
    if not documents:
        print("\n❌ Aucun document à indexer!")
        print("\n💡 Ajoutez des fichiers PDF, Word, Excel ou texte dans:")
        print(f"   {Config.DOCUMENTS_DIR}")
        return
    
    # 2. Découper en chunks
    print("\n" + "=" * 60)
    chunks = chunk_documents(documents)
    
    # 3. Créer le vectorstore
    print("\n" + "=" * 60)
    vectorstore = create_vectorstore(chunks)
    
    # Statistiques finales
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("✨ INGESTION TERMINÉE AVEC SUCCÈS!")
    print("=" * 60)
    print(f"📊 Statistiques:")
    print(f"   • Documents traités: {len(documents)}")
    print(f"   • Chunks créés: {len(chunks)}")
    print(f"   • Temps d'exécution: {elapsed_time:.2f}s")
    print(f"   • Vectorstore: {Config.VECTORSTORE_DIR}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    ingest_documents()