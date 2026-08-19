# src/student_profile.py

import json
from typing import List, Dict, Optional
from datetime import datetime


class StudentProfile:
    """
    Tracks student learning progress, weak areas, and mastery
    """

    def __init__(self, student_id: str, grade: int = 8, name: str = ""):
        self.id = student_id
        self.name = name
        self.grade = grade

        # Performance tracking
        self.quiz_scores: Dict[str, List[float]] = {}
        self.quiz_attempts: Dict[str, int] = {}
        self.question_history: List[Dict] = []

        # Topics
        self.weak_topics: List[str] = []
        self.mastered_topics: List[str] = []
        self.studied_topics: List[str] = []

        # Learning preferences
        self.difficulty_level: int = 1  # 1-3
        self.hint_level: int = 1  # 1-3

        # Engagement
        self.session_count: int = 0
        self.total_time_spent: float = 0
        self.last_active: str = datetime.now().isoformat()
        self.created_at: str = datetime.now().isoformat()

    def add_quiz_score(self, topic: str, score: float, max_score: float = 100) -> Dict:
        """Add a quiz score and update topic mastery"""
        normalized = (score / max_score) * 100

        if topic not in self.quiz_scores:
            self.quiz_scores[topic] = []
        self.quiz_scores[topic].append(normalized)

        if topic not in self.quiz_attempts:
            self.quiz_attempts[topic] = 0
        self.quiz_attempts[topic] += 1

        avg = sum(self.quiz_scores[topic]) / len(self.quiz_scores[topic])

        status_changes = {
            'topic': topic,
            'score': normalized,
            'average': avg,
            'attempts': self.quiz_attempts[topic]
        }

        if avg >= 80:
            if topic not in self.mastered_topics:
                self.mastered_topics.append(topic)
                status_changes['status'] = 'mastered'
            if topic in self.weak_topics:
                self.weak_topics.remove(topic)
        elif avg < 60:
            if topic not in self.weak_topics:
                self.weak_topics.append(topic)
                status_changes['status'] = 'weak'
            if topic in self.mastered_topics:
                self.mastered_topics.remove(topic)
        else:
            status_changes['status'] = 'learning'

        self.last_active = datetime.now().isoformat()
        return status_changes

    def add_question(self, question: str, answer: str, topic: str):
        """Record a question-answer interaction"""
        self.question_history.append({
            'question': question,
            'answer': answer[:200],
            'topic': topic,
            'timestamp': datetime.now().isoformat()
        })

        if topic not in self.studied_topics:
            self.studied_topics.append(topic)

    def get_weakest_topics(self, n: int = 3) -> List[str]:
        """Get the n weakest topics"""
        if not self.weak_topics:
            return []

        topic_scores = {
            topic: sum(scores) / len(scores)
            for topic, scores in self.quiz_scores.items()
            if topic in self.weak_topics
        }
        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1])
        return [topic for topic, _ in sorted_topics[:n]]

    def get_recommendations(self) -> Dict:
        """Get personalized learning recommendations"""
        weak = self.get_weakest_topics(3)

        recommendations = {
            'focus_on': weak,
            'next_challenge': self.mastered_topics[-1] if self.mastered_topics else None,
            'practice_more': weak,
            'suggested_difficulty': min(self.difficulty_level + 1, 3) if not weak else self.difficulty_level
        }

        if not weak and self.mastered_topics:
            recommendations['message'] = "Great progress! Try increasing difficulty."
        elif weak:
            recommendations['message'] = f"Focus on: {', '.join(weak)}"
        else:
            recommendations['message'] = "Keep learning new topics!"

        return recommendations

    def get_progress_summary(self) -> Dict:
        """Get comprehensive progress summary"""
        total_quizzes = sum(self.quiz_attempts.values())
        avg_score = sum([sum(s) for s in self.quiz_scores.values()]) / max(1,
                                                                           len(self.quiz_scores)) if self.quiz_scores else 0

        return {
            'student_id': self.id,
            'name': self.name,
            'grade': self.grade,
            'weak_topics': self.weak_topics,
            'mastered_topics': self.mastered_topics,
            'studied_topics': self.studied_topics,
            'total_quizzes': total_quizzes,
            'average_score': round(avg_score, 1),
            'total_questions': len(self.question_history),
            'session_count': self.session_count,
            'difficulty_level': self.difficulty_level,
            'recommendations': self.get_recommendations(),
            'last_active': self.last_active
        }

    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'name': self.name,
            'grade': self.grade,
            'quiz_scores': self.quiz_scores,
            'quiz_attempts': self.quiz_attempts,
            'weak_topics': self.weak_topics,
            'mastered_topics': self.mastered_topics,
            'studied_topics': self.studied_topics,
            'difficulty_level': self.difficulty_level,
            'hint_level': self.hint_level,
            'session_count': self.session_count,
            'total_time_spent': self.total_time_spent,
            'last_active': self.last_active,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'StudentProfile':
        """Create from dictionary"""
        profile = cls(data['id'], data.get('grade', 8), data.get('name', ''))
        profile.quiz_scores = data.get('quiz_scores', {})
        profile.quiz_attempts = data.get('quiz_attempts', {})
        profile.weak_topics = data.get('weak_topics', [])
        profile.mastered_topics = data.get('mastered_topics', [])
        profile.studied_topics = data.get('studied_topics', [])
        profile.difficulty_level = data.get('difficulty_level', 1)
        profile.hint_level = data.get('hint_level', 1)
        profile.session_count = data.get('session_count', 0)
        profile.total_time_spent = data.get('total_time_spent', 0)
        profile.last_active = data.get('last_active', datetime.now().isoformat())
        profile.created_at = data.get('created_at', datetime.now().isoformat())
        return profile

    def save(self, filepath: str):
        """Save profile to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> 'StudentProfile':
        """Load profile from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)