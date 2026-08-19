# src/tutor.py

import requests
import re
from typing import Dict, Optional, List
from datetime import datetime

from src.config import (
    OPENROUTER_API_KEY,
    MODELS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    CHAPTER_TOPICS
)
from src.knowledge_base_chroma import KnowledgeBase
from src.student_profile import StudentProfile
from src.utils import truncate_text


class AITutor:
    """
    Personalized AI Tutor for NCERT Science (Classes 8, 9, 10)
    """

    def __init__(self, folder: str = "./data", api_key: str = None):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.knowledge = KnowledgeBase(folder)
        self.students: Dict[str, StudentProfile] = {}

        if not self.api_key or self.api_key == "your-key-here":
            print("⚠️ Please set OPENROUTER_API_KEY in config.py or pass api_key")

    # ============================================================
    # Student Management
    # ============================================================

    def get_student(self, student_id: str) -> StudentProfile:
        """Get or create student profile"""
        if student_id not in self.students:
            self.students[student_id] = StudentProfile(student_id)
        return self.students[student_id]

    # ============================================================
    # Core Methods
    # ============================================================

    def explain(self,
                concept: str,
                student_id: Optional[str] = None,
                grade: Optional[str] = None) -> Dict:
        """
        Explain a concept with grade-aware personalization
        """
        student = None
        difficulty = 1

        if student_id:
            student = self.get_student(student_id)
            difficulty = student.difficulty_level
            if not grade:
                grade = f"Class {student.grade}"

        if not grade:
            grade = "Class 9"

        diff_levels = ["simple", "moderate", "advanced"]
        diff_idx = min(difficulty - 1, 2)
        diff_text = diff_levels[diff_idx]

        # Search with grade awareness
        topics = self._extract_topics(concept)
        results = self.knowledge.search(concept, topics=topics, grade=grade, top_k=4)

        if not results:
            results = self.knowledge.search(concept, topics=topics, top_k=4)

        context = "\n\n".join([r['text'] for r in results]) if results else ""
        sources = [r['metadata'].get('chapter', 'Unknown') for r in results[:2]]
        source_grades = [r['metadata'].get('grade', 'Unknown') for r in results[:2]]

        grade_text = grade.replace("Class ", "")
        system_prompt = f"""You are a personalized AI tutor for NCERT Science (Classes 8-10).
Student Grade: {grade}
Explanation Level: {diff_text}
Use appropriate language for this grade level."""

        user_prompt = f"""CONCEPT: {concept}

NCERT CONTEXT:
{context}

INSTRUCTIONS:
1. Explain in {diff_text} language suitable for {grade}
2. Break down complex ideas
3. Include real-world examples
4. End with a follow-up question
5. Be encouraging and patient

EXPLANATION:"""

        try:
            response = self._call_api(system_prompt, user_prompt, temperature=0.4, max_tokens=DEFAULT_MAX_TOKENS)

            # Check for valid response
            if not response or 'choices' not in response or not response['choices']:
                return {
                    'concept': concept,
                    'explanation': 'No response from the AI model. Please try again.',
                    'error': True
                }

            answer = response['choices'][0]['message']['content']

            if student:
                student.add_question(concept, answer, concept)

            return {
                'concept': concept,
                'explanation': answer,
                'follow_up': self._generate_follow_up(concept),
                'level': diff_text,
                'grade': grade,
                'sources': sources,
                'source_grades': source_grades,
                'student_id': student_id
            }

        except Exception as e:
            return {
                'concept': concept,
                'explanation': f"⚠️ Error: {str(e)}",
                'error': True
            }

    def ask_by_grade(self, question: str, grade: str) -> Dict:
        """Ask a question restricted to a specific grade"""
        return self.explain(question, grade=grade)

    def hint(self, question: str, student_id: Optional[str] = None) -> Dict:
        """Provide a progressive hint"""
        student = None
        hint_level = 2

        if student_id:
            student = self.get_student(student_id)
            hint_level = student.hint_level

        hint_types = ["subtle", "moderate", "detailed"]
        hint_type = hint_types[min(hint_level - 1, 2)]

        results = self.knowledge.search(question, top_k=3)
        context = "\n".join([r['text'] for r in results]) if results else ""

        system_prompt = f"You are a helpful tutor. Give a {hint_type} hint without revealing the full answer."

        user_prompt = f"""QUESTION: {question}

CONTEXT: {context}

HINT LEVEL: {hint_type}

Provide a hint that guides thinking without giving the full answer.

HINT:"""

        try:
            response = self._call_api(system_prompt, user_prompt, model='fast', temperature=0.6, max_tokens=200)
            hint_text = response['choices'][0]['message']['content']

            return {
                'question': question,
                'hint': hint_text,
                'level': hint_type,
                'next_step': "Try to solve it now. Ask for another hint if needed."
            }

        except Exception as e:
            return {
                'question': question,
                'hint': "Think about what you know from NCERT. Review the relevant chapter.",
                'error': True
            }

    def quiz(self, topic: str, num_questions: int = 3, difficulty: int = 1,
             student_id: Optional[str] = None) -> Dict:
        """Generate a personalized quiz"""
        diff_texts = ["Basic", "Moderate", "Challenging"]
        diff_text = diff_texts[min(difficulty - 1, 2)]

        results = self.knowledge.search(topic, top_k=3)
        context = "\n".join([r['text'] for r in results]) if results else ""

        system_prompt = f"You are a quiz generator for NCERT Science."

        user_prompt = f"""Create a {diff_text} quiz on "{topic}" for NCERT Science.

CONTEXT:
{context}

Generate {num_questions} questions with a mix of MCQs and short answers.
Include answer key with explanations.

FORMAT:
### Questions
Q1. [MCQ] Question
a) Option A
b) Option B
c) Option C
d) Option D
Answer: [Correct option]
Explanation: [Brief explanation]

Q2. [Short Answer] Question
Answer: [Answer]
Explanation: [Brief explanation]

QUIZ:"""

        try:
            response = self._call_api(system_prompt, user_prompt, temperature=0.5, max_tokens=800, timeout=35)
            quiz_text = response['choices'][0]['message']['content']

            return {
                'topic': topic,
                'quiz': quiz_text,
                'difficulty': diff_text,
                'num_questions': num_questions,
                'student_id': student_id
            }

        except Exception as e:
            return {
                'topic': topic,
                'quiz': f"⚠️ Error: {str(e)}",
                'error': True
            }

    def progress(self, student_id: str) -> Dict:
        """Get student progress summary"""
        student = self.get_student(student_id)
        return student.get_progress_summary()

    def recommend(self, student_id: str) -> Dict:
        """Get personalized recommendations"""
        student = self.get_student(student_id)
        return student.get_recommendations()

    def compare_across_grades(self, concept: str) -> Dict:
        """Compare how a concept is taught across grades"""
        results = {}
        for grade in ["Class 8", "Class 9", "Class 10"]:
            result = self.explain(concept, grade=grade)
            results[grade] = {
                'explanation': result['explanation'],
                'level': result.get('level', 'moderate')
            }
        return {
            'concept': concept,
            'comparison': results,
            'progression': self._get_progression(concept, results)
        }

    # ============================================================
    # Private Methods
    # ============================================================

    def _call_api(self, system_prompt: str, user_prompt: str,
                  model: str = None, temperature: float = None,
                  max_tokens: int = None, timeout: int = 45) -> Dict:
        """Make API call to OpenRouter"""
        model = model or DEFAULT_MODEL
        temperature = temperature or DEFAULT_TEMPERATURE
        max_tokens = max_tokens or DEFAULT_MAX_TOKENS

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5000",
                    "X-Title": "AI Tutor NCERT"
                },
                json={
                    "model": MODELS.get(model, MODELS['free']),
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=timeout
            )

            response.raise_for_status()
            result = response.json()

            if 'choices' not in result or not result['choices']:
                print(f"⚠️ No choices in response: {result}")
                return {'choices': [{'message': {'content': 'No response from model'}}]}

            return result

        except requests.exceptions.Timeout:
            print(f"⚠️ API timeout after {timeout}s")
            return {'choices': [{'message': {'content': 'Request timed out. Please try again.'}}]}

        except requests.exceptions.RequestException as e:
            print(f"⚠️ API error: {e}")
            return {'choices': [{'message': {'content': f'API error: {str(e)}'}}]}

        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            return {'choices': [{'message': {'content': f'Error: {str(e)}'}}]}

    def _generate_follow_up(self, concept: str) -> str:
        """Generate a follow-up question"""
        prompt = f"Generate a simple, encouraging follow-up question about '{concept}' for a student."

        try:
            response = self._call_api("You are a helpful tutor.", prompt,
                                      model='fast', temperature=0.7, max_tokens=50, timeout=10)
            return response['choices'][0]['message']['content']
        except:
            return f"Can you think of an example of '{concept}' from your daily life?"

    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        from src.config import CHAPTER_TOPICS
        text_lower = text.lower()
        matched = []

        for chapter, topics in CHAPTER_TOPICS.items():
            for topic in topics:
                if topic.lower() in text_lower:
                    matched.append(topic)

        return list(set(matched))[:3]

    def _get_progression(self, concept: str, results: Dict) -> str:
        """Analyze progression across grades"""
        levels = []
        for grade in ["Class 8", "Class 9", "Class 10"]:
            if grade in results:
                levels.append(results[grade].get('level', 'medium'))
        if len(levels) >= 3:
            if levels[0] == "simple" and levels[1] == "moderate" and levels[2] == "advanced":
                return f"Concept '{concept}' shows clear progression from simple to advanced across grades."
            elif levels[0] == levels[1] == levels[2]:
                return f"Concept '{concept}' is taught at similar level across all grades."
        return f"Concept '{concept}' is covered at varying levels across grades."