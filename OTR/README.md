# 🤖 OTR Chatbot - Assistant Intelligent

Chatbot intelligent pour l'Organisation Togolaise des Receveurs (OTR) permettant d'interroger facilement tous les documents internes.

## ✨ Fonctionnalités

- 💬 **Chat conversationnel** avec mémoire des échanges
- ⚡ **Réponses ultra-rapides** grâce au système de cache intelligent
- 📚 **Support multi-formats**: PDF, Word, Excel, PowerPoint, TXT
- 🔍 **Recherche sémantique** dans tous les documents
- 📊 **Tableau de bord** avec statistiques d'utilisation
- 🎨 **Interface moderne** et intuitive avec Streamlit
- 🚀 **API REST** pour intégrations tierces

## 🛠️ Technologies utilisées

- **LangChain**: Orchestration du chatbot
- **OpenRouter**: Hébergement du modèle IA (Claude Haiku)
- **ChromaDB**: Base de données vectorielle (rapide et locale)
- **Sentence Transformers**: Embeddings locaux (gratuit)
- **Streamlit**: Interface utilisateur
- **FastAPI**: API REST

## 📦 Installation

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd OTR_CHAT
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration

Créez un fichier `.env` à la racine avec vos clés API:
```env
OPENROUTER_API_KEY=votre_clé_ici
MODEL_NAME=anthropic/claude-3-haiku
```

Obtenez votre clé API sur: https://openrouter.ai/

## 🚀 Utilisation

### Étape 1: Ajouter vos documents

Placez tous vos documents (PDF, Word, Excel, etc.) dans le dossier:
```
OTR/data/documents/
```

### Étape 2: Indexer les documents
```bash
python OTR/scripts/ingest.py
```

Cette commande va:
- Charger tous les documents
- Les découper en chunks intelligents
- Créer les embeddings
- Sauvegarder dans ChromaDB

### Étape 3: Lancer l'interface Streamlit
```bash
streamlit run OTR/frontend/streamlit.py
```

L'interface s'ouvrira automatiquement dans votre navigateur à: `http://localhost:8501`

### Option: Lancer l'API REST
```bash
python OTR/api/main.py
```

L'API sera accessible à: `http://localhost:8000`

Documentation interactive: `http://localhost:8000/docs`

## 📖 Guide d'utilisation

### Interface Chat

1. Tapez votre question dans la zone de saisie
2. Appuyez sur Entrée
3. Le chatbot recherche dans les documents et répond
4. Les sources sont affichées sous la réponse

**Fonctionnalités spéciales:**
- Le chatbot se souvient de la conversation
- Questions de suivi possibles
- Réponses en cache = instantanées
- Suggestions de questions

### Gestion des documents

Accédez à l'onglet "📚 Documents" pour:
- Voir tous les documents indexés
- Consulter les statistiques
- Rechercher un document spécifique

### Statistiques

L'onglet "📊 Statistiques" affiche:
- Nombre total de questions
- Performance du cache
- Temps de réponse moyen
- Taux de cache hit

## 🔌 Utilisation de l'API

### Poser une question
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Qu'est-ce que l'OTR?"}'
```

### Obtenir les statistiques
```bash
curl "http://localhost:8000/stats"
```

### Effacer la mémoire conversationnelle
```bash
curl -X POST "http://localhost:8000/clear"
```

## 📁 Structure du projet
```
OTR_CHAT/
├── OTR/
│   ├── agentAI/              # Logique du chatbot
│   │   ├── chatbot.py        # Agent principal
│   │   ├── cache.py          # Système de cache
│   │   └── response_optimizer.py
│   ├── api/                  # API REST
│   │   └── main.py
│   ├── data/                 # Données
│   │   ├── documents/        # Documents sources
│   │   ├── vectorestore/     # Base vectorielle
│   │   ├── cache/            # Cache des réponses
│   │   └── conversations.json
│   ├── frontend/             # Interface Streamlit
│   │   ├── streamlit.py
│   │   └── components/
│   └── scripts/              # Scripts utilitaires
│       ├── config.py
│       ├── ingest.py
│       ├── storage.py
│       └── chuncking.py
├── .env
├── requirements.txt
└── README.md
```

## ⚙️ Configuration avancée

Modifiez le fichier `.env` pour personnaliser:
```env
# Modèle IA (plus rapide ou plus intelligent)
MODEL_NAME=anthropic/claude-3-haiku  # Rapide
# MODEL_NAME=anthropic/claude-3-sonnet  # Équilibré
# MODEL_NAME=anthropic/claude-3-opus  # Plus intelligent

# Taille des chunks
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Nombre de documents à récupérer
RETRIEVAL_K=3

# Durée du cache (en secondes)
CACHE_TTL=3600
```

## 🐛 Résolution de problèmes

### Erreur "No documents found"

- Vérifiez que les documents sont dans `OTR/data/documents/`
- Relancez `python OTR/scripts/ingest.py`

### Erreur de clé API

- Vérifiez que le fichier `.env` existe
- Vérifiez que votre clé OpenRouter est valide

### Réponses lentes

- Utilisez un modèle plus rapide (claude-3-haiku)
- Réduisez `RETRIEVAL_K` dans le `.env`
- Les réponses en cache sont instantanées

### Chatbot ne se souvient pas

- La mémoire est limitée à une conversation
- Cliquez sur "Effacer la conversation" pour recommencer

## 📈 Performances

- **Première question**: 2-5 secondes (recherche + génération)
- **Questions en cache**: < 0.01 seconde (instantané)
- **Capacité**: Supporte des milliers de documents
- **Mémoire conversationnelle**: Illimitée dans une session

## 🤝 Contribution

Les contributions sont les bienvenues! 

## 📄 Licence

MIT License

## 👥 Contact

Pour toute question ou suggestion:
- Email: contact@otr.tg
- GitHub: [Issues](https://github.com/votre-repo/issues)

---

**Développé avec ❤️ pour l'OTR**