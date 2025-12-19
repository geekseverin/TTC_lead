"""
Découpage intelligent des documents en chunks
"""
import sys
from pathlib import Path

# Ajouter le chemin parent
sys.path.append(str(Path(__file__).parent.parent))

from langchain.text_splitter import RecursiveCharacterTextSplitter
from scripts.config import Config

def chunk_documents(documents):
    """
    Découpe les documents en chunks optimisés
    Utilise RecursiveCharacterTextSplitter pour préserver le contexte
    """
    print(f"✂️  Découpage des documents en chunks...")
    print(f"   Taille: {Config.CHUNK_SIZE} | Overlap: {Config.CHUNK_OVERLAP}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(documents)
    
    print(f"✅ {len(chunks)} chunks créés")
    return chunks

def chunk_text(text, chunk_size=None, chunk_overlap=None):
    """Découpe un texte brut en chunks"""
    if chunk_size is None:
        chunk_size = Config.CHUNK_SIZE
    if chunk_overlap is None:
        chunk_overlap = Config.CHUNK_OVERLAP
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    return text_splitter.split_text(text)