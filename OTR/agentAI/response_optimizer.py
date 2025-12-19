"""
Optimiseur de réponses - Ultra concis
"""
import re

class ResponseOptimizer:
    def __init__(self):
        pass
    
    def optimize(self, response, sources=None):
        """Optimise la réponse"""
        # 1. Nettoyer
        response = self._clean_text(response)
        
        # 2. Enlever répétitions
        response = self._remove_duplicates(response)
        
        # 3. Ultra concis
        response = self._make_ultra_concise(response)
        
        # 4. Ajouter sources (MAX 2)
        if sources:
            response = self._add_sources(response, sources[:2])
        
        return response
    
    def _clean_text(self, text):
        """Nettoie"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _remove_duplicates(self, text):
        """Enlève répétitions"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        unique = []
        seen = set()
        
        for s in sentences:
            norm = s.lower().strip()
            if norm and norm not in seen and len(norm) > 10:
                unique.append(s)
                seen.add(norm)
        
        return ' '.join(unique)
    
    def _make_ultra_concise(self, text):
        """Ultra bref"""
        # Max 200 caractères
        if len(text) > 200:
            sentences = text.split('.')
            text = '. '.join(sentences[:2]) + '.'
        
        return text.strip()
    
    def _add_sources(self, response, sources):
        """Ajoute sources (max 2)"""
        if not sources:
            return response
        
        unique = []
        seen = set()
        
        for s in sources:
            filename = s.get('filename', 'Document')
            if filename not in seen:
                unique.append(filename)
                seen.add(filename)
        
        if unique:
            response += "\n\n📚 **Sources:**\n"
            for i, src in enumerate(unique[:2], 1):
                response += f"{i}. {src}\n"
        
        return response