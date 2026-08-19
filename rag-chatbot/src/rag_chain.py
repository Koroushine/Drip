# src/rag_chain.py - RAG Chain (Legacy/Compat layer)

"""
This file provides backward compatibility for the RAG chain.
It's essentially a wrapper around the KnowledgeBase and Tutor.
"""

from src.knowledge_base import KnowledgeBase
from src.tutor import AITutor
from src.config import DATA_FOLDER, DEFAULT_TOP_K


class RAGChain:
    """
    Legacy RAG chain for backward compatibility
    Actually just wraps KnowledgeBase for simpler API
    """

    def __init__(self, folder: str = DATA_FOLDER):
        self.knowledge = KnowledgeBase(folder)
        self.tutor = AITutor(folder)

    def search(self, query: str, top_k: int = DEFAULT_TOP_K):
        """Search knowledge base"""
        return self.knowledge.search(query, top_k=top_k)

    def ask(self, question: str):
        """Simple question answering (no personalization)"""
        return self.tutor.explain(question)

    def get_context(self, query: str, top_k: int = DEFAULT_TOP_K) -> str:
        """Get context for a query"""
        results = self.knowledge.search(query, top_k=top_k)
        return "\n\n".join([r['text'] for r in results])

    def get_stats(self):
        """Get knowledge base stats"""
        return self.knowledge.get_stats()