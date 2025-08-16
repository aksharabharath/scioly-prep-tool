import json
import random
import os
import time

DATA_FILE = "questions.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_question(data):
    question = input("Enter question: ")
    answer = input("Enter answer: ")
    topic = input("Enter topic (e.g., Astronomy, Forensics): ")
    difficulty = input("Enter difficulty (Easy, Medium, Hard): ")

    data.append({
        "question": question,
        "answer": answer,
        "topic": topic,
        "difficulty": difficulty
    })
    save_data(data)
    print("✅ Question added successfully!\n")

def view_questions(data):
    if not data:
        print("⚠️ No questions available.\n")
        return
    for i, q in enumerate(data, 1):
        print(f"{i}. {q['question']} (Topic: {q['topic']}, Difficulty: {q['difficulty']})")
    print()

def study_mode(data):
    if not data:
        print("⚠️ No questions available.\n")
        return

    print("🎯 Study Mode - Practice Freely")
    questions = data[:]
    random.shuffle(questions)

    for q in questions:
        print(f"\nQuestion: {q['question']}")
        input("Press Enter to see the answer...")
        print(f"Answer: {q['answer']}")
        input("Press Enter to continue...")

def timed_drill(data):
    if not data:
        print("⚠️ No questions available.\n")
        return

    topic_filter = input("Filter by topic (or press Enter for all): ")
    difficulty_filter = input("Filter by difficulty (Easy, Medium, Hard, or press Enter for all): ")

    filtered = [
        q for q in data
        if (not topic_filter or q['topic'].lower() == topic_filter.lower())
        and (not difficulty_filter or q['difficulty'].lower() == difficulty_filter.lower())
    ]

    if not filtered:
        print("⚠️ No questions match your filter.\n")
        return

    random.shuffle(filtered)

    num_questions = len(filtered)
    recommended_time = num_questions  # minutes (1 min per question)

    print(f"\nNumber of questions selected: {num_questions}")
    print(f"Recommended time: {recommended_time} minutes (1 min per question)\n")

    print("Choose your time setting:")
    print("1. Use recommended time")
    print("2. Enter your own time")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        time_limit = recommended_time
    else:
        try:
            time_limit = int(input("Enter time limit in minutes: "))
        except ValueError:
            print("⚠️ Invalid input. Using recommended time instead.")
            time_limit = recommended_time

    print(f"\n⏳ Timed Drill Started! You have {time_limit} minutes.\n")

    start_time = time.time()
    time_limit_seconds = time_limit * 60

    for q in filtered:
        elapsed = time.time() - start_time
        remaining = time_limit_seconds - elapsed
        if remaining <= 0:
            print("\n⏰ Time's up! Drill ended.\n")
            break

        print(f"Question: {q['question']}")
        input("Press Enter to see the answer...")
        print(f"Answer: {q['answer']}")
        print(f"⏱ Remaining time: {int(remaining // 60)} min {int(remaining % 60)} sec\n")

def main():
    data = load_data()

    while True:
        print("=== SciOly Prep Tool ===")
        print("1. Add Question")
        print("2. View Questions")
        print("3. Study Mode")
        print("4. Timed Drill")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_question(data)
        elif choice == "2":
            view_questions(data)
        elif choice == "3":
            study_mode(data)
        elif choice == "4":
            timed_drill(data)
        elif choice == "5":
            print("👋 Exiting... Good luck studying!")
            break
        else:
            print("⚠️ Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
