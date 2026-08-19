# demo.py - Quick demonstration for your paper

from src.tutor import AITutor
from src.config import OPENROUTER_API_KEY


def main():
    print("\n" + "=" * 60)
    print("🧠 NCERT AI TUTOR - Personalized Learning")
    print("Classes 8, 9, 10")
    print("=" * 60)

    if OPENROUTER_API_KEY == "your-openrouter-api-key-here":
        print("\n⚠️ Please set OPENROUTER_API_KEY in src/config.py")
        return

    print("\n📚 Loading...")
    tutor = AITutor()

    # Questions by grade
    questions = [
        ("Class 8", "What is a cell?"),
        ("Class 9", "What is Newton's first law of motion?"),
        ("Class 10", "What is Ohm's law?"),
    ]

    print("\n" + "-" * 60)

    for grade, question in questions:
        print(f"\n📖 {grade}")
        print(f"Q: {question}")

        result = tutor.ask_by_grade(question, grade)

        if result.get('error'):
            print(f"A: Error - {result.get('explanation')}")
        else:
            print(f"A: {result['explanation'][:200]}...")
            if result.get('sources'):
                print(f"📚 Source: {result['sources'][0]}")

    print("\n" + "=" * 60)
    print("✅ Demo complete! Your AI Tutor is ready.")
    print("Run: python test_chatbot.py --quick for more tests")


if __name__ == "__main__":
    main()