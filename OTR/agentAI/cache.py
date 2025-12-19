"""
Système de cache intelligent pour réponses rapides
"""
import json
import hashlib
import time
from pathlib import Path
from scripts.config import Config

class QuestionCache:
    def __init__(self):
        self.cache_file = Config.CACHE_DIR / "responses.json"
        self.stats_file = Config.CACHE_DIR / "stats.json"
        self.cache = self._load_cache()
        self.stats = self._load_stats()
    
    def _load_cache(self):
        """Charge le cache depuis le fichier"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Sauvegarde le cache"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def _load_stats(self):
        """Charge les statistiques"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._init_stats()
        return self._init_stats()
    
    def _init_stats(self):
        """Initialise les statistiques"""
        return {
            'total_questions': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_response_time': 0
        }
    
    def _save_stats(self):
        """Sauvegarde les statistiques"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2)
    
    def _normalize_question(self, question):
        """Normalise une question pour la recherche"""
        return question.lower().strip()
    
    def _get_key(self, question):
        """Crée une clé unique pour chaque question"""
        normalized = self._normalize_question(question)
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, question):
        """Récupère une réponse du cache"""
        key = self._get_key(question)
        
        if key in self.cache:
            data = self.cache[key]
            
            # Vérifier l'expiration (TTL)
            if time.time() - data['timestamp'] < Config.CACHE_TTL:
                # Incrémenter les stats
                data['hit_count'] = data.get('hit_count', 0) + 1
                self.stats['cache_hits'] += 1
                self._save_cache()
                self._save_stats()
                
                print("⚡ Réponse du cache (instantané!)")
                return data['response']
            else:
                # Cache expiré
                del self.cache[key]
                self._save_cache()
        
        self.stats['cache_misses'] += 1
        self._save_stats()
        return None
    
    def set(self, question, response, response_time=0):
        """Ajoute une réponse au cache"""
        key = self._get_key(question)
        
        self.cache[key] = {
            'question': question,
            'response': response,
            'timestamp': time.time(),
            'hit_count': 0,
            'response_time': response_time
        }
        
        # Limiter la taille du cache
        if len(self.cache) > Config.CACHE_MAX_SIZE:
            # Supprimer les entrées les moins utilisées
            sorted_items = sorted(
                self.cache.items(),
                key=lambda x: (x[1].get('hit_count', 0), x[1]['timestamp'])
            )
            self.cache = dict(sorted_items[-Config.CACHE_MAX_SIZE:])
        
        self._save_cache()
    
    def update_stats(self, response_time):
        """Met à jour les statistiques"""
        self.stats['total_questions'] += 1
        self.stats['total_response_time'] += response_time
        self._save_stats()
    
    def get_stats(self):
        """Retourne les statistiques"""
        stats = self.stats.copy()
        if stats['total_questions'] > 0:
            stats['cache_hit_rate'] = (stats['cache_hits'] / stats['total_questions']) * 100
            stats['average_response_time'] = stats['total_response_time'] / stats['total_questions']
        else:
            stats['cache_hit_rate'] = 0
            stats['average_response_time'] = 0
        
        return stats
    
    def clear(self):
        """Vide le cache"""
        self.cache = {}
        self._save_cache()
        print("🗑️  Cache vidé")