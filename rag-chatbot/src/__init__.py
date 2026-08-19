# src/__init__.py

from src.knowledge_base_chroma import KnowledgeBase
from src.tutor import AITutor
from src.student_profile import StudentProfile
from src.config import OPENROUTER_API_KEY, MODELS

__all__ = [
    'AITutor',
    'StudentProfile',
    'KnowledgeBase',
    'OPENROUTER_API_KEY',
    'MODELS'
]

__version__ = '1.0.0'
__project__ = "AI Tutor"