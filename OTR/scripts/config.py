"""
Configuration centralisée du chatbot OTR
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    # Chemins
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DOCUMENTS_DIR = DATA_DIR / "documents"
    VECTORSTORE_DIR = DATA_DIR / "vectorestore"
    CACHE_DIR = DATA_DIR / "cache"
    CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "anthropic/claude-3-haiku")
    
    # Embedding Configuration (local, gratuit)
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Chunking Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    
    # Retrieval Configuration
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", 3))
    
    # Cache Configuration
    CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
    CACHE_MAX_SIZE = 500
    
    # Températures
    TEMPERATURE = 0.0  # Pour des réponses cohérentes
    
    @classmethod
    def create_directories(cls):
        """Crée tous les dossiers nécessaires"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.DOCUMENTS_DIR.mkdir(exist_ok=True)
        cls.VECTORSTORE_DIR.mkdir(exist_ok=True)
        cls.CACHE_DIR.mkdir(exist_ok=True)
        
        # Créer le fichier conversations s'il n'existe pas
        if not cls.CONVERSATIONS_FILE.exists():
            import json
            with open(cls.CONVERSATIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)

# Créer les dossiers au démarrage
Config.create_directories()