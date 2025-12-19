"""
Chatbot OTR principal avec mémoire conversationnelle
Version optimisée - Style institutionnel professionnel
"""

import sys
import time
import re
import httpx
from pathlib import Path

# Ajouter le chemin parent
sys.path.append(str(Path(__file__).parent.parent))

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from scripts.storage import load_vectorstore
from scripts.config import Config
from agentAI.cache import QuestionCache
from agentAI.response_optimizer import ResponseOptimizer


class OTRChatbot:
    """
    Chatbot intelligent pour l’Office Togolais des Recettes (OTR)
    - Réponses fiables basées sur documents internes
    - Mémoire conversationnelle
    - Cache des questions fréquentes
    - Anti-hallucination stricte
    """

    def __init__(self):
        print("🚀 Initialisation du chatbot OTR...")

        # Cache & Optimisation
        self.cache = QuestionCache()
        self.optimizer = ResponseOptimizer()

        # Charger le vectorstore
        print("📚 Chargement de la base de connaissances...")
        self.vectorstore = load_vectorstore()

        # Client HTTP
        http_client = httpx.Client(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )

        # Modèle LLM
        print("🤖 Configuration du modèle IA...")
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            api_key=Config.OPENROUTER_API_KEY,
            base_url=Config.OPENROUTER_BASE_URL,
            temperature=Config.TEMPERATURE,
            streaming=False,
            http_client=http_client
        )

        # Mémoire conversationnelle
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        # Prompt
        self.prompt = self._create_prompt()

        # Chaîne conversationnelle
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={"k": Config.RETRIEVAL_K, "fetch_k": 10}
            ),
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self.prompt},
            verbose=False
        )

        print("✅ Chatbot OTR prêt\n")

    # ------------------------------------------------------------------
    # PROMPT
    # ------------------------------------------------------------------
    def _create_prompt(self):
        template = """
Tu es un assistant conversationnel officiel de l’Office Togolais des Recettes (OTR).

RÈGLE PRINCIPALE :
Tu dois répondre UNIQUEMENT à partir des informations contenues dans les documents fournis.
Il est strictement interdit d’inventer, de supposer ou de compléter une information manquante.

RAISONNEMENT AUTORISÉ :
Tu peux reformuler, relier des termes similaires ou combiner plusieurs extraits pertinents
si et seulement si ces informations sont explicitement présentes dans les documents.

SI L’INFORMATION EST ABSENTE :
Réponds clairement que l’information n’est pas disponible dans les documents OTR.

CONVERSATION COURANTE :
Réponds poliment aux salutations (bonjour, merci, etc.).

STYLE :
- Professionnel et institutionnel
- Clair et accessible au grand public
- 2 à 4 phrases maximum sauf demande explicite

INTERDICTIONS :
- Pas d’avis personnel
- Pas d’informations juridiques/fiscales non présentes
- Pas de chiffres, lois ou délais non mentionnés

CONTEXTE :
{context}

HISTORIQUE :
{chat_history}

QUESTION :
{question}

RÉPONSE :
"""
        return PromptTemplate(
            template=template,
            input_variables=["context", "chat_history", "question"]
        )

    # ------------------------------------------------------------------
    # QUESTION PRINCIPALE
    # ------------------------------------------------------------------
    def ask(self, question: str) -> dict:
        start_time = time.time()

        # Questions simples
        simple = self._handle_simple_questions(question)
        if simple:
            return simple

        # Cache
        cached = self.cache.get(question)
        if cached:
            return {
                "answer": cached,
                "sources": [],
                "from_cache": True,
                "response_time": 0.001
            }

        try:
            print("🔍 Recherche documentaire OTR...")
            response = self.qa_chain.invoke({"question": question})

            answer = response.get("answer", "")
            source_docs = response.get("source_documents", [])

            answer = self._clean_response(answer)
            sources = [doc.metadata for doc in source_docs]

            final_answer = self.optimizer.optimize(answer, sources)
            response_time = time.time() - start_time

            self.cache.set(question, final_answer, response_time)
            self.cache.update_stats(response_time)

            return {
                "answer": final_answer,
                "sources": sources,
                "from_cache": False,
                "response_time": response_time
            }

        except Exception as e:
            print("❌ Erreur :", e)
            return {
                "answer": "Une erreur est survenue. Veuillez réessayer.",
                "sources": [],
                "from_cache": False,
                "response_time": time.time() - start_time
            }

    # ------------------------------------------------------------------
    # QUESTIONS SIMPLES
    # ------------------------------------------------------------------
    def _handle_simple_questions(self, question: str):
        q = question.lower().strip()

        if q in ["bonjour", "salut", "hello", "bonsoir"]:
            return {
                "answer": "Bonjour, comment puis-je vous aider concernant les services de l’OTR ?",
                "sources": [],
                "from_cache": False,
                "response_time": 0.001
            }

        if "merci" in q:
            return {
                "answer": "Je vous en prie. N’hésitez pas si vous avez d’autres questions.",
                "sources": [],
                "from_cache": False,
                "response_time": 0.001
            }

        return None

    # ------------------------------------------------------------------
    # NETTOYAGE DES RÉPONSES
    # ------------------------------------------------------------------
    def _clean_response(self, text: str) -> str:
        phrases_interdites = [
            "D'après les extraits fournis",
            "Selon le contexte",
            "Il est important de noter que",
            "Cependant",
            "En effet"
        ]

        for p in phrases_interdites:
            text = text.replace(p, "")

        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) < 10:
            return "Je n’ai pas cette information dans les documents de l’OTR."

        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return '. '.join(sentences[:4]) + '.'

    # ------------------------------------------------------------------
    # UTILITAIRES
    # ------------------------------------------------------------------
    def clear_memory(self):
        self.memory.clear()

    def get_conversation_history(self):
        return self.memory.load_memory_variables({})

    def get_cache_stats(self):
        return self.cache.get_stats()
