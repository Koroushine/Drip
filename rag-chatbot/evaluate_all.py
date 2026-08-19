# evaluate_all.py - Fixed version

import json
import time
from src.tutor import AITutor

print("🚀 RUNNING ALL EVALUATIONS")
print("=" * 60)

# ============================================================
# LOAD CORPUS (ONCE)
# ============================================================

print("\n📚 Loading corpus...")
start_load = time.time()
tutor = AITutor()  # ← Create tutor here
print(f"✅ Corpus loaded in {time.time() - start_load:.1f}s")
print(f"   Total chunks: {len(tutor.knowledge.chunks)}")

# ============================================================
# 1. RETRIEVAL ACCURACY
# ============================================================

print("\n" + "=" * 60)
print("📊 1. RETRIEVAL ACCURACY")
print("=" * 60)

GROUND_TRUTH = {
    "What is a cell?": {
        "expected_chapters": ["hecu102.pdf", "iesc102.pdf", "jesc105.pdf"],
        "expected_grade": "Class 8"
    },
    "What is Newton's first law?": {
        "expected_chapters": ["iesc106.pdf", "jesc106.pdf"],
        "expected_grade": "Class 9"
    },
    "What is Ohm's law?": {
        "expected_chapters": ["jesc111.pdf"],
        "expected_grade": "Class 10"
    },
    "What is photosynthesis?": {
        "expected_chapters": ["hecu102.pdf", "jesc105.pdf"],
        "expected_grade": "Class 8"
    },
    "What is a chemical reaction?": {
        "expected_chapters": ["jesc101.pdf"],
        "expected_grade": "Class 10"
    }
}

retrieval_results = []
correct_chapter = 0
correct_grade = 0

for question, truth in GROUND_TRUTH.items():
    results = tutor.knowledge.search(question, top_k=3)
    retrieved_chapters = [r['metadata'].get('file', '') for r in results]
    retrieved_grades = [r['metadata'].get('grade', '') for r in results]

    found_chapter = any(exp in retrieved_chapters for exp in truth['expected_chapters'])
    found_grade = truth['expected_grade'] in retrieved_grades

    if found_chapter:
        correct_chapter += 1
    if found_grade:
        correct_grade += 1

    retrieval_results.append({
        'question': question,
        'found_chapter': found_chapter,
        'found_grade': found_grade
    })
    print(f"  ✅ {question[:30]}... → Chapter: {found_chapter}, Grade: {found_grade}")

print(f"\nChapter Retrieval Accuracy: {correct_chapter / len(GROUND_TRUTH) * 100:.1f}%")
print(f"Grade Detection Accuracy: {correct_grade / len(GROUND_TRUTH) * 100:.1f}%")

# ============================================================
# 2. ANSWER ACCURACY
# ============================================================

print("\n" + "=" * 60)
print("📊 2. ANSWER ACCURACY")
print("=" * 60)

KEYWORD_TESTS = {
    "What is a cell?": {
        "keywords": ["cell", "basic", "unit", "life", "living"],
        "grade": "Class 8"
    },
    "What is Newton's first law?": {
        "keywords": ["rest", "motion", "force", "constant", "velocity"],
        "grade": "Class 9"
    },
    "What is Ohm's law?": {
        "keywords": ["current", "voltage", "resistance", "ohm"],
        "grade": "Class 10"
    },
    "What is photosynthesis?": {
        "keywords": ["sunlight", "carbon dioxide", "water", "oxygen"],
        "grade": "Class 8"
    }
}

answer_results = []
answer_scores = []

for question, test in KEYWORD_TESTS.items():
    result = tutor.ask_by_grade(question, test['grade'])
    answer = result.get('explanation', '').lower()

    found = [kw for kw in test['keywords'] if kw.lower() in answer]
    missing = [kw for kw in test['keywords'] if kw.lower() not in answer]
    score = len(found) / len(test['keywords']) * 100
    answer_scores.append(score)

    answer_results.append({
        'question': question,
        'found': found,
        'missing': missing,
        'score': score
    })
    print(f"  ✅ {question[:30]}... → {len(found)}/{len(test['keywords'])} keywords ({score:.0f}%)")

avg_answer_score = sum(answer_scores) / len(answer_scores) if answer_scores else 0
print(f"\nAverage Answer Accuracy: {avg_answer_score:.1f}%")

# ============================================================
# 3. SYSTEM PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("📊 3. SYSTEM PERFORMANCE")
print("=" * 60)

stats = tutor.knowledge.get_stats()
print(f"Total Chunks: {stats['total_chunks']}")
print(f"Loaded Files: {stats['loaded_files']}")
print(f"Class 8: {stats['grade_counts']['Class 8']} chunks")
print(f"Class 9: {stats['grade_counts']['Class 9']} chunks")
print(f"Class 10: {stats['grade_counts']['Class 10']} chunks")

# ============================================================
# 4. QUIZ QUALITY (FIXED - uses tutor)
# ============================================================

print("\n" + "=" * 60)
print("📊 4. QUIZ QUALITY")
print("=" * 60)

quiz_topics = ["cell structure", "electricity", "force"]
quiz_scores = []

for topic in quiz_topics:
    print(f"\n  Generating quiz for: {topic}")

    try:
        result = tutor.quiz(topic, num_questions=2)  # ← tutor is defined!
        quiz_text = result.get('quiz', '')

        if not quiz_text:
            print(f"  ⚠️ No quiz generated for {topic}")
            quiz_scores.append(0)
            continue

        has_q = '?' in str(quiz_text)
        has_mcq = 'a)' in str(quiz_text).lower()
        has_answer = 'answer' in str(quiz_text).lower()
        has_explain = 'explain' in str(quiz_text).lower()

        score = sum([has_q, has_mcq, has_answer, has_explain]) / 4 * 100
        quiz_scores.append(score)

        print(f"  ✅ {topic}: {score:.0f}%")
        print(f"     Questions: {has_q}, MCQs: {has_mcq}, Answers: {has_answer}, Explanations: {has_explain}")
        print(f"     Preview: {str(quiz_text)[:100]}...")

    except Exception as e:
        print(f"  ❌ Error for {topic}: {e}")
        quiz_scores.append(0)

avg_quiz_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0
print(f"\nAverage Quiz Quality: {avg_quiz_score:.1f}%")

# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("📊 FINAL RESULTS SUMMARY")
print("=" * 60)

results_summary = {
    'retrieval_chapter_accuracy': correct_chapter / len(GROUND_TRUTH) * 100,
    'retrieval_grade_accuracy': correct_grade / len(GROUND_TRUTH) * 100,
    'answer_accuracy': avg_answer_score,
    'quiz_quality': avg_quiz_score,
    'total_chunks': stats['total_chunks'],
    'loaded_files': stats['loaded_files']
}

print(json.dumps(results_summary, indent=2))

# Save results
with open('evaluation_results.json', 'w') as f:
    json.dump({
        'summary': results_summary,
        'retrieval': retrieval_results,
        'answers': answer_results,
        'quiz': quiz_scores
    }, f, indent=2)

print("\n✅ Results saved to evaluation_results.json")
print(f"Total time: {time.time() - start_load:.1f}s")