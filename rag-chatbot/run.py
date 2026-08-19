# run.py - Simple interactive runner

from src.tutor import AITutor
from src.config import OPENROUTER_API_KEY


def main():
    print("\n" + "=" * 50)
    print("🧠 NCERT AI TUTOR")
    print("Ask any science question (Class 8-10)")
    print("Type 'exit' to quit")
    print("=" * 50)

    if OPENROUTER_API_KEY == "your-openrouter-api-key-here":
        print("\n⚠️ Please set OPENROUTER_API_KEY in src/config.py")
        return

    print("\n📚 Loading knowledge base...")
    tutor = AITutor()
    print("✅ Ready!")

    while True:
        print("\n" + "-" * 50)
        question = input("📝 Your question: ").strip()

        if question.lower() in ['exit', 'quit', 'q']:
            print("👋 Goodbye!")
            break

        if not question:
            continue

        print("\n🤔 Thinking...")
        result = tutor.explain(question)

        if result.get('error'):
            print(f"❌ Error: {result.get('explanation')}")
        else:
            print(f"\n💡 Answer:\n{result['explanation']}")

            if result.get('sources'):
                print(f"\n📚 Sources: {', '.join(result['sources'][:2])}")


if __name__ == "__main__":
    main()