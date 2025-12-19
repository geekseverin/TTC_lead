"""
API FastAPI pour le chatbot OTR
Permet d'accéder au chatbot via des endpoints REST
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
from pathlib import Path

# Ajouter le chemin parent pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from agentAI.chatbot import OTRChatbot
from scripts.config import Config

# Initialiser FastAPI
app = FastAPI(
    title="OTR Chatbot API",
    description="API pour interroger les documents de l'Organisation Togolaise des Receveurs",
    version="1.0.0"
)

# Configuration CORS pour accès depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser le chatbot (une seule fois au démarrage)
chatbot = None

@app.on_event("startup")
async def startup_event():
    """Initialise le chatbot au démarrage du serveur"""
    global chatbot
    print("🚀 Démarrage de l'API OTR Chatbot...")
    chatbot = OTRChatbot()
    print("✅ API prête à recevoir des requêtes\n")

# Modèles Pydantic pour la validation des données
class Question(BaseModel):
    question: str
    
class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
    from_cache: bool
    response_time: float

class StatsResponse(BaseModel):
    total_questions: int
    cache_hits: int
    cache_misses: int
    cache_hit_rate: float
    average_response_time: float

# Endpoints
@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "API OTR Chatbot",
        "status": "active",
        "endpoints": {
            "/ask": "POST - Poser une question",
            "/health": "GET - Vérifier l'état de l'API",
            "/stats": "GET - Obtenir les statistiques",
            "/clear": "POST - Effacer la mémoire conversationnelle",
            "/docs": "GET - Documentation interactive"
        }
    }

@app.get("/health")
async def health_check():
    """Vérifie l'état de santé de l'API"""
    return {
        "status": "healthy",
        "chatbot_ready": chatbot is not None,
        "model": Config.MODEL_NAME,
        "vectorstore": str(Config.VECTORSTORE_DIR)
    }

@app.post("/ask", response_model=ChatResponse)
async def ask_question(question: Question):
    """
    Pose une question au chatbot
    
    Args:
        question: La question à poser
    
    Returns:
        ChatResponse avec la réponse et les sources
    """
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot non initialisé")
    
    if not question.question.strip():
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide")
    
    try:
        response = chatbot.ask(question.question)
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Retourne les statistiques d'utilisation du chatbot"""
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot non initialisé")
    
    try:
        stats = chatbot.get_cache_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/clear")
async def clear_memory():
    """Efface la mémoire conversationnelle"""
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot non initialisé")
    
    try:
        chatbot.clear_memory()
        return {"message": "Mémoire conversationnelle effacée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/history")
async def get_history():
    """Retourne l'historique de la conversation en cours"""
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot non initialisé")
    
    try:
        history = chatbot.get_conversation_history()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Lancement du serveur API...")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)