# test_chatbot.py - Comprehensive Test for Class 8, 9, 10

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tutor import AITutor
from src.config import OPENROUTER_API_KEY, TEST_QUESTIONS, CHAPTER_NAMES


# ============================================================
# Color codes for terminal output
# ============================================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    print(f"\n{Colors.HEADER}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.HEADER}{'=' * 70}{Colors.END}")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_info(text):
    print(f"{Colors.BLUE}ℹ️ {text}{Colors.END}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.END}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


# ============================================================
# Test Functions
# ============================================================

def test_knowledge_base():
    """Test if all PDFs are loaded correctly"""
    print_header("📚 TEST 1: KNOWLEDGE BASE LOADING")

    bot = AITutor()
    stats = bot.knowledge.get_stats()

    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Loaded files: {stats['loaded_files']}/{stats['total_files']}")
    print(f"Grade counts:")
    for grade, count in stats['grade_counts'].items():
        print(f"  - {grade}: {count} chunks")

    if stats['total_chunks'] > 0:
        print_success(f"Knowledge base loaded successfully!")
    else:
        print_error("No chunks loaded! Check if PDFs are in data/ folder.")

    return bot


def test_grade_specific_questions(bot):
    """Test questions specific to each grade"""
    print_header("📝 TEST 2: GRADE-SPECIFIC QUESTIONS")

    test_data = [
        ("Class 8", "What is a cell?"),
        ("Class 9", "What is the difference between distance and displacement?"),
        ("Class 10", "What is Ohm's law?"),
        ("Class 8", "What are the three states of matter?"),
        ("Class 9", "What is Newton's first law of motion?"),
        ("Class 10", "What is the pH scale?"),
    ]

    results = []

    for grade, question in test_data:
        print(f"\n{Colors.YELLOW}Grade: {grade}{Colors.END}")
        print(f"Question: {question}")
        print("-" * 40)

        try:
            result = bot.ask_by_grade(question, grade)

            if result.get('error'):
                print_error(f"Error: {result.get('explanation')}")
                results.append(False)
            else:
                print(f"Answer: {result['explanation'][:300]}...")
                if result.get('sources'):
                    print(f"Sources: {', '.join(result['sources'][:2])}")
                if result.get('grade'):
                    print(f"Grade used: {result['grade']}")
                print_success("Question answered successfully!")
                results.append(True)
        except Exception as e:
            print_error(f"Exception: {e}")
            results.append(False)

    success_rate = sum(results) / len(results) * 100
    print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.END}")

    return results


def test_cross_grade_comparison(bot):
    """Test comparing concepts across grades"""
    print_header("📊 TEST 3: CROSS-GRADE COMPARISON")

    concepts = ["cell", "force", "light", "electricity", "reproduction"]

    for concept in concepts[:3]:  # Test first 3 concepts
        print(f"\n{Colors.BOLD}Concept: {concept}{Colors.END}")
        print("-" * 40)

        try:
            result = bot.compare_across_grades(concept)

            if result.get('error'):
                print_error(f"Error: {result}")
            else:
                for grade, data in result['comparison'].items():
                    level = data.get('level', 'moderate')
                    explanation = data['explanation'][:150] + "..."
                    print(f"\n  {Colors.GREEN}{grade} (Level: {level}){Colors.END}")
                    print(f"    {explanation}")

                print(f"\n  {Colors.BLUE}Progression: {result.get('progression', 'N/A')}{Colors.END}")
                print_success("Comparison completed!")
        except Exception as e:
            print_error(f"Exception: {e}")


def test_detailed_answer(bot):
    """Test detailed answers with citations"""
    print_header("🔬 TEST 4: DETAILED ANSWERS WITH CITATIONS")

    question = "Explain the process of photosynthesis in detail."

    print(f"Question: {question}")
    print("-" * 40)

    try:
        result = bot.explain(question, grade="Class 10")

        if result.get('error'):
            print_error(f"Error: {result.get('explanation')}")
        else:
            print(f"\n{Colors.BOLD}Answer:{Colors.END}\n{result['explanation']}")

            if result.get('sources'):
                print(f"\n{Colors.BOLD}Sources:{Colors.END}")
                for i, source in enumerate(result['sources'], 1):
                    grade = result.get('source_grades', ['Unknown'])[i - 1] if result.get(
                        'source_grades') else 'Unknown'
                    print(f"  {i}. {source} ({grade})")

            if result.get('follow_up'):
                print(f"\n{Colors.BOLD}Follow-up:{Colors.END} {result['follow_up']}")

            print_success("Detailed answer generated!")
    except Exception as e:
        print_error(f"Exception: {e}")


def test_student_profiles(bot):
    """Test student profile tracking"""
    print_header("👤 TEST 5: STUDENT PROFILE TRACKING")

    # Create students
    students = {
        "student_weak": {"name": "Ravi", "grade": 8, "weak": ["photosynthesis", "electricity"]},
        "student_advanced": {"name": "Priya", "grade": 10, "mastered": ["force", "light", "cell"]},
    }

    for student_id, info in students.items():
        print(f"\n{Colors.BOLD}Student: {info['name']} (Grade {info['grade']}){Colors.END}")

        # Get or create profile
        student = bot.get_student(student_id)
        student.name = info['name']
        student.grade = info['grade']

        if info.get('weak'):
            student.weak_topics = info['weak']
            print(f"  Weak topics: {', '.join(info['weak'])}")

        if info.get('mastered'):
            student.mastered_topics = info['mastered']
            print(f"  Mastered topics: {', '.join(info['mastered'])}")

        # Ask a question with this student
        print(f"  Asking: 'What is a cell?'")
        result = bot.explain("What is a cell?", student_id=student_id)

        if result.get('error'):
            print_error(f"Error: {result.get('explanation')}")
        else:
            print(f"  Level used: {result.get('level', 'moderate')}")
            print(f"  Answer: {result['explanation'][:200]}...")
            print_success(f"Personalized for {info['name']}!")

        # Show progress
        summary = student.get_progress_summary()
        print(f"  Progress: {summary.get('average_score', 0):.1f}% average")
        print(f"  Total quizzes: {summary.get('total_quizzes', 0)}")


def test_quiz_generation(bot):
    """Test quiz generation"""
    print_header("📝 TEST 6: QUIZ GENERATION")

    quiz_configs = [
        ("Cell Structure", 3, 1),
        ("Electricity", 3, 2),
        ("Force and Motion", 2, 1),
    ]

    for topic, num_questions, difficulty in quiz_configs:
        print(f"\n{Colors.BOLD}Topic: {topic}{Colors.END}")
        print(f"Questions: {num_questions} | Difficulty: {difficulty}")
        print("-" * 40)

        try:
            result = bot.quiz(topic, num_questions=num_questions, difficulty=difficulty)

            if result.get('error'):
                print_error(f"Error: {result.get('quiz')}")
            else:
                print(f"\n{result['quiz']}")
                print_success(f"Quiz generated!")
        except Exception as e:
            print_error(f"Exception: {e}")


def test_performance(bot):
    """Test response time"""
    print_header("⚡ TEST 7: PERFORMANCE")

    import time

    test_questions = [
        "What is a cell?",
        "Explain Newton's laws",
        "What is photosynthesis?",
        "Explain Ohm's law",
        "What is the structure of DNA?",
    ]

    times = []

    for i, question in enumerate(test_questions, 1):
        print(f"  {i}. {question[:50]}...", end=" ", flush=True)

        start = time.time()
        result = bot.explain(question)
        elapsed = time.time() - start

        if result.get('error'):
            print(f"{Colors.RED}Failed{Colors.END}")
        else:
            print(f"{Colors.GREEN}{elapsed:.2f}s{Colors.END}")
            times.append(elapsed)

    if times:
        avg = sum(times) / len(times)
        print(f"\n{Colors.BOLD}Average response time: {avg:.2f}s{Colors.END}")


def test_comprehensive_question(bot):
    """Test a comprehensive question that might span multiple grades"""
    print_header("🎯 TEST 8: COMPREHENSIVE QUESTION")

    question = "What is the difference between plant and animal cells? How does this relate to their functions?"

    print(f"Question: {question}")
    print("-" * 40)

    try:
        # Ask without grade restriction to get best answer
        result = bot.explain(question)

        if result.get('error'):
            print_error(f"Error: {result.get('explanation')}")
        else:
            print(f"\n{Colors.BOLD}Answer:{Colors.END}\n{result['explanation']}")

            if result.get('sources'):
                print(f"\n{Colors.BOLD}Sources:{Colors.END}")
                for i, source in enumerate(result['sources'], 1):
                    grade = result.get('source_grades', ['Unknown'])[i - 1] if result.get(
                        'source_grades') else 'Unknown'
                    print(f"  {i}. {source} ({grade})")

            print_success("Comprehensive question answered!")
    except Exception as e:
        print_error(f"Exception: {e}")


def test_topic_search(bot):
    """Test topic-based search"""
    print_header("🔍 TEST 9: TOPIC SEARCH")

    topics = ["cell", "force", "light", "electricity", "heredity"]

    for topic in topics:
        print(f"\n{Colors.BOLD}Topic: {topic}{Colors.END}")
        print("-" * 30)

        try:
            results = bot.knowledge.search(topic, top_k=3)

            if results:
                print(f"  Found {len(results)} relevant chunks:")
                for i, result in enumerate(results, 1):
                    meta = result.get('metadata', {})
                    chapter = meta.get('chapter', 'Unknown')
                    grade = meta.get('grade', 'Unknown')
                    score = result.get('score', 0)
                    text = result['text'][:100] + "..."
                    print(f"    {i}. {chapter} ({grade}) - Score: {score:.3f}")
                    print(f"       {text}")
                print_success("Topic search successful!")
            else:
                print_warning(f"No results for topic: {topic}")
        except Exception as e:
            print_error(f"Exception: {e}")


# ============================================================
# Main Test Runner
# ============================================================

def run_all_tests():
    """Run all tests"""

    print(f"\n{Colors.HEADER}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🧠 NCERT AI TUTOR - COMPREHENSIVE TEST SUITE{Colors.END}")
    print(f"Class 8, 9, 10 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.HEADER}{'=' * 70}{Colors.END}")

    # Check API key
    if OPENROUTER_API_KEY == "your-openrouter-api-key-here":
        print_error("Please set OPENROUTER_API_KEY in src/config.py")
        print("Get it from: https://openrouter.ai/keys")
        return

    # Initialize bot
    print_info("Initializing AI Tutor...")
    bot = AITutor()

    # Run tests
    test_knowledge_base(bot)
    test_grade_specific_questions(bot)
    test_cross_grade_comparison(bot)
    test_detailed_answer(bot)
    test_student_profiles(bot)
    test_quiz_generation(bot)
    test_performance(bot)
    test_comprehensive_question(bot)
    test_topic_search(bot)

    print_header("✅ ALL TESTS COMPLETE!")
    print("Your AI Tutor for NCERT Class 8, 9, 10 is ready!")


def quick_test():
    """Quick test with 3 questions only"""

    print(f"\n{Colors.HEADER}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}⚡ QUICK TEST (3 Questions){Colors.END}")
    print(f"{Colors.HEADER}{'=' * 70}{Colors.END}")

    if OPENROUTER_API_KEY == "your-openrouter-api-key-here":
        print_error("Please set OPENROUTER_API_KEY in src/config.py")
        return

    bot = AITutor()

    questions = [
        ("Class 8", "What is a cell?"),
        ("Class 9", "What is Newton's first law of motion?"),
        ("Class 10", "What is Ohm's law?"),
    ]

    for grade, question in questions:
        print(f"\n{Colors.YELLOW}📖 {grade}{Colors.END}")
        print(f"Q: {question}")
        print("-" * 40)

        result = bot.ask_by_grade(question, grade)

        if result.get('error'):
            print_error(f"Error: {result.get('explanation')}")
        else:
            print(f"A: {result['explanation'][:250]}...")
            if result.get('sources'):
                print(f"📚 Sources: {', '.join(result['sources'][:2])}")
            print_success("Done!")


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test NCERT AI Tutor")
    parser.add_argument("--quick", action="store_true", help="Run quick test only")
    parser.add_argument("--full", action="store_true", help="Run full test suite")

    args = parser.parse_args()

    if args.quick:
        quick_test()
    else:
        run_all_tests()