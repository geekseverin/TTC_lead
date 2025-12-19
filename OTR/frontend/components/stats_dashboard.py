"""
Tableau de bord des statistiques d'utilisation
"""
import streamlit as st
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.config import Config

def load_stats():
    """Charge les statistiques depuis le fichier"""
    stats_file = Config.CACHE_DIR / "stats.json"
    
    if stats_file.exists():
        try:
            with open(stats_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {
        'total_questions': 0,
        'cache_hits': 0,
        'cache_misses': 0,
        'total_response_time': 0
    }

def calculate_metrics(stats):
    """Calcule les métriques dérivées"""
    total = stats['total_questions']
    
    if total == 0:
        return {
            'cache_hit_rate': 0,
            'cache_miss_rate': 0,
            'avg_response_time': 0
        }
    
    return {
        'cache_hit_rate': (stats['cache_hits'] / total) * 100,
        'cache_miss_rate': (stats['cache_misses'] / total) * 100,
        'avg_response_time': stats['total_response_time'] / total if total > 0 else 0
    }

def render_stats_cards():
    """Affiche les cartes de statistiques principales"""
    stats = load_stats()
    metrics = calculate_metrics(stats)
    
    # Première ligne de métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Questions totales",
            value=stats['total_questions'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="⚡ Depuis le cache",
            value=stats['cache_hits'],
            delta=f"{metrics['cache_hit_rate']:.1f}%" if stats['total_questions'] > 0 else None
        )
    
    with col3:
        st.metric(
            label="🔍 Nouvelles recherches",
            value=stats['cache_misses'],
            delta=None
        )
    
    with col4:
        st.metric(
            label="⏱️ Temps moyen",
            value=f"{metrics['avg_response_time']:.2f}s",
            delta=None
        )

def render_cache_performance():
    """Affiche la performance du cache"""
    stats = load_stats()
    metrics = calculate_metrics(stats)
    
    st.subheader("⚡ Performance du cache")
    
    if stats['total_questions'] == 0:
        st.info("Aucune statistique disponible. Posez des questions pour voir les performances!")
        return
    
    # Barre de progression
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.progress(metrics['cache_hit_rate'] / 100)
        st.write(f"**Taux de cache hit:** {metrics['cache_hit_rate']:.1f}%")
        
        # Interprétation
        if metrics['cache_hit_rate'] > 50:
            st.success("✅ Excellente performance! Le cache fonctionne bien.")
        elif metrics['cache_hit_rate'] > 25:
            st.info("ℹ️ Performance correcte. Plus de questions répétées amélioreront le cache.")
        else:
            st.warning("⚠️ Les questions sont très variées. C'est normal au début.")
    
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 10px;
                    color: white;
                    text-align: center;'>
            <h2 style='margin: 0;'>{stats['cache_hits']}</h2>
            <p style='margin: 5px 0 0 0;'>Réponses instantanées</p>
        </div>
        """, unsafe_allow_html=True)

def render_response_time_analysis():
    """Analyse des temps de réponse"""
    stats = load_stats()
    metrics = calculate_metrics(stats)
    
    st.subheader("⏱️ Analyse des temps de réponse")
    
    if stats['total_questions'] == 0:
        st.info("Pas encore de données disponibles.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Temps moyen de réponse:**
        """)
        if metrics['avg_response_time'] < 2:
            st.success(f"🚀 Très rapide: {metrics['avg_response_time']:.2f}s")
        elif metrics['avg_response_time'] < 5:
            st.info(f"⚡ Rapide: {metrics['avg_response_time']:.2f}s")
        else:
            st.warning(f"🐌 Peut être amélioré: {metrics['avg_response_time']:.2f}s")
    
    with col2:
        # Estimation du gain de temps grâce au cache
        if stats['cache_hits'] > 0:
            time_saved = stats['cache_hits'] * metrics['avg_response_time']
            st.markdown(f"""
            <div style='background-color: #10b981; 
                        padding: 15px; 
                        border-radius: 10px;
                        color: white;'>
                <strong>⏳ Temps économisé par le cache:</strong><br>
                <h3 style='margin: 5px 0;'>{time_saved:.1f}s</h3>
            </div>
            """, unsafe_allow_html=True)

def render_full_dashboard():
    """Affiche le tableau de bord complet"""
    st.title("📊 Tableau de bord - Statistiques OTR Chatbot")
    
    # Cartes de statistiques
    render_stats_cards()
    
    st.markdown("---")
    
    # Performance du cache
    col1, col2 = st.columns(2)
    
    with col1:
        render_cache_performance()
    
    with col2:
        render_response_time_analysis()
    
    st.markdown("---")
    
    # Informations système
    st.subheader("🔧 Informations système")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **Modèle IA:**  
        {Config.MODEL_NAME}
        """)
    
    with col2:
        st.info(f"""
        **Embedding:**  
        {Config.EMBEDDING_MODEL.split('/')[-1]}
        """)
    
    with col3:
        st.info(f"""
        **Vectorstore:**  
        ChromaDB
        """)

def render_stats_sidebar():
    """Affiche un résumé des stats dans la sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📊 Statistiques")
    
    stats = load_stats()
    metrics = calculate_metrics(stats)
    
    st.sidebar.metric("Questions", stats['total_questions'])
    
    if stats['total_questions'] > 0:
        st.sidebar.progress(metrics['cache_hit_rate'] / 100)
        st.sidebar.caption(f"Cache: {metrics['cache_hit_rate']:.0f}% hit rate")
    
    if st.sidebar.button("📊 Voir détails", use_container_width=True):
        st.session_state.page = 'stats'