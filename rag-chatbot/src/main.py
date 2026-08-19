# src/main.py - Main entry point

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tutor import AITutor
from src.student_profile import StudentProfile
from src.config import OPENROUTER_API_KEY, TEST_QUESTIONS


def run_demo():
    """Run comprehensive demo for the AI Tutor"""

    print("\n" + "=" * 70)
    print("🧠 AI TUTOR - NCERT Class 8 Science")
    print("Research: Personalized AI-Assisted Science Education")
    print("=" * 70)

    # Check API key
    if OPENROUTER_API_KEY == "your-openrouter-api-key-here":
        print("\n⚠️ Please set OPENROUTER_API_KEY in src/config.py")
        print("Get it from: https://openrouter.ai/keys")
        return

    # Initialize
    tutor = AITutor()

    # Student profiles
    s1 = "student_struggling"
    s2 = "student_advanced"
    s3 = "student_test"

    # Demo 1: Personalized Explanations
    print("\n" + "=" * 70)
    print("1️⃣ PERSONALIZED EXPLANATIONS")
    print("=" * 70)

    # Set up struggling student
    tutor.students[s1] = StudentProfile(s1, name="Ravi")
    tutor.students[s1].weak_topics = ["photosynthesis", "electricity"]
    tutor.students[s1].difficulty_level = 1

    # Set up advanced student
    tutor.students[s2] = StudentProfile(s2, name="Priya")
    tutor.students[s2].mastered_topics = ["force", "light", "cell"]
    tutor.students[s2].difficulty_level = 3

    concept = "Photosynthesis"
    print(f"\n📖 CONCEPT: {concept}")

    for student_id, student in tutor.students.items():
        print(f"\n🎓 {student.name} (Level {student.difficulty_level}):")
        result = tutor.explain(concept, student_id)
        print(f"   Level: {result.get('level', 'moderate')}")
        print(f"   {result['explanation'][:350]}...")
        print(f"   🔍 Follow-up: {result.get('follow_up', '')}")

    # Demo 2: Progressive Hints
    print("\n" + "=" * 70)
    print("2️⃣ PROGRESSIVE HINTS")
    print("=" * 70)

    question = "What happens when you increase the number of turns in an electromagnet?"
    print(f"\n❓ QUESTION: {question}")

    for hint_level in [1, 2, 3]:
        hint_result = tutor.hint(question, s1)
        print(f"\n🔍 Hint Level {hint_level} ({hint_result.get('level', 'moderate')}):")
        print(f"   {hint_result['hint']}")

    # Demo 3: Quiz Generation
    print("\n" + "=" * 70)
    print("3️⃣ QUIZ GENERATION")
    print("=" * 70)

    quiz_result = tutor.quiz("Electricity", num_questions=3, difficulty=2, student_id=s1)
    print(f"\n📝 TOPIC: {quiz_result['topic']}")
    print(f"📊 Difficulty: {quiz_result.get('difficulty', 'Moderate')}")
    print(f"\n{quiz_result['quiz'][:500]}...")

    # Demo 4: Progress Tracking
    print("\n" + "=" * 70)
    print("4️⃣ PROGRESS TRACKING")
    print("=" * 70)

    # Simulate quiz attempts
    print("\n📊 Simulating student progress...")
    student = tutor.get_student("test_progress")

    # First attempt - fails
    print("   Quiz 1: 'Force' - Score: 40%")
    student.add_quiz_score("force", 40)
    print(f"   Weak topics: {student.weak_topics}")

    # Second attempt - improves
    print("   Quiz 2: 'Force' - Score: 65%")
    student.add_quiz_score("force", 65)
    print(f"   Weak topics: {student.weak_topics}")

    # Third attempt - masters
    print("   Quiz 3: 'Force' - Score: 85%")
    student.add_quiz_score("force", 85)
    print(f"   Mastered topics: {student.mastered_topics}")

    # Progress summary
    summary = student.get_progress_summary()
    print(f"\n📈 Progress Summary:")
    print(f"   Weak topics: {summary['weak_topics']}")
    print(f"   Mastered topics: {summary['mastered_topics']}")
    print(f"   Average score: {summary['average_score']:.1f}%")
    print(f"   Total quizzes: {summary['total_quizzes']}")

    # Recommendations
    print("\n🎯 Recommendations:")
    recommendations = tutor.recommend("test_progress")
    print(f"   {recommendations.get('message', 'Keep learning!')}")

    # Demo 5: Sample outputs from different chapters
    print("\n" + "=" * 70)
    print("5️⃣ SAMPLE OUTPUTS - DIFFERENT CHAPTERS")
    print("=" * 70)

    sample_questions = [
        ("Cell", "What is a cell?"),
        ("Health", "How do vaccines work?"),
        ("Force", "What is the difference between mass and weight?"),
        ("Light", "How do lenses work?")
    ]

    for topic, question in sample_questions:
        print(f"\n📖 {topic}: {question}")
        result = tutor.explain(question)
        print(f"   {result['explanation'][:250]}...")

    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE - Ready for your paper!")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()