# scioly_prep_tool.py
import streamlit as st
import random
import time
import json

# ------------------------------
# Load Questions JSON
# ------------------------------
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Organize questions by event
questions_by_event = {}
for q in all_questions:
    event = q.get("event", "Unknown Event")
    if event not in questions_by_event:
        questions_by_event[event] = []
    questions_by_event[event].append(q)

# ------------------------------
# Streamlit App
# ------------------------------
st.title("Science Olympiad Prep Tool")

# Initialize session state
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'scores' not in st.session_state:
    st.session_state.scores = {}

# Sidebar options
event = st.selectbox("Select Event:", list(questions_by_event.keys()))
mode = st.radio("Select Mode:", ["Study Mode", "Timed Drill"])

# Topic Filtering: use 'topic' or fallback to 'subtopic'
event_questions = questions_by_event[event]
topics = list(set(q.get('topic', q.get('subtopic', 'Unknown')) for q in event_questions))
topics = [t for t in topics if t != 'Unknown']
selected_topics = st.multiselect("Filter by Topic:", topics, default=topics)

# Difficulty Filtering
difficulties = list(set(q['difficulty'] for q in event_questions))
selected_difficulty = st.multiselect("Select Difficulty:", difficulties, default=difficulties)

# Filter questions based on selection
filtered_questions = [
    q for q in event_questions
    if (q.get('topic', q.get('subtopic', 'Unknown')) in selected_topics)
    and (q['difficulty'] in selected_difficulty)
]
random.shuffle(filtered_questions)

# ------------------------------
# Timed Drill / Study Mode
# ------------------------------
if mode == "Timed Drill":
    time_limit = st.number_input("Enter time limit in seconds:", min_value=30, value=60)
    start_drill = st.button("Start Timed Drill")
    if start_drill:
        start_time = time.time()
        for i, q in enumerate(filtered_questions, 1):
            elapsed = time.time() - start_time
            if elapsed > time_limit:
                st.warning("Time's up!")
                break
            st.write(f"**Q{i}: {q['question']}**")
            choice = st.radio("Select answer:", q["options"], key=f"{event}_{i}")
            show_hint = st.checkbox("Show Hint", key=f"hint_{i}")
            if show_hint:
                st.info(q.get("hint", "No hint available."))
            if st.button(f"Submit Q{i}", key=f"submit_{event}_{i}"):
                if choice == q["answer"]:
                    st.success("Correct!")
                    st.session_state.scores[event] = st.session_state.scores.get(event, 0) + 1
                else:
                    st.error(f"Incorrect! Correct answer: {q['answer']}")
                entry = f"Q{i}: {q['question']} - Answer: {q['answer']}"
                if entry not in st.session_state.selected_questions:
                    st.session_state.selected_questions.append(entry)
else:
    # Study Mode
    for i, q in enumerate(filtered_questions, 1):
        st.write(f"**Q{i}: {q['question']}**")
        choice = st.radio("Select answer:", q["options"], key=f"{event}_{i}")
        show_hint = st.checkbox("Show Hint", key=f"hint_{i}")
        if show_hint:
            st.info(q.get("hint", "No hint available."))
        if st.button(f"Submit Q{i}", key=f"submit_{event}_{i}"):
            if choice == q["answer"]:
                st.success("Correct!")
                st.session_state.scores[event] = st.session_state.scores.get(event, 0) + 1
            else:
                st.error(f"Incorrect! Correct answer: {q['answer']}")
            entry = f"Q{i}: {q['question']} - Answer: {q['answer']}"
            if entry not in st.session_state.selected_questions:
                st.session_state.selected_questions.append(entry)

# ------------------------------
# Cheat Sheet
# ------------------------------
if st.button("Generate Cheat Sheet"):
    if st.session_state.selected_questions:
        cheat_text = "\n".join(st.session_state.selected_questions)
        st.write("### Cheat Sheet")
        st.text(cheat_text)
        st.download_button("Download Cheat Sheet", cheat_text, file_name=f"{event}_cheatsheet.txt")
    else:
        st.warning("No questions answered yet!")

# Reset Progress
if st.button("Reset Progress"):
    st.session_state.selected_questions = []
    st.session_state.scores[event] = 0
    st.success("Progress reset!")

# Display Scores / Progress Analytics
st.write("### Your Scores")
for e, score in st.session_state.scores.items():
    st.write(f"{e}: {score} correct answers")

# ------------------------------
# Timed Drill / Study Mode
# ------------------------------
if mode == "Timed Drill":
    time_limit = st.number_input("Enter total time limit in seconds:", min_value=30, value=120)
    start_drill = st.button("Start Timed Drill")
    
    if start_drill:
        # Save start time in session state
        st.session_state.start_time = time.time()
        st.session_state.time_limit = time_limit
        st.session_state.current_q_index = 0

    if 'start_time' in st.session_state:
        elapsed = time.time() - st.session_state.start_time
        remaining_time = st.session_state.time_limit - elapsed

        if remaining_time <= 0:
            st.warning("⏰ Time's up!")
        else:
            st.info(f"Time remaining: {int(remaining_time)} seconds")

            # Show current question
            if st.session_state.current_q_index < len(filtered_questions):
                q = filtered_questions[st.session_state.current_q_index]
                st.write(f"**Q{st.session_state.current_q_index + 1}: {q['question']}**")
                choice = st.radio("Select answer:", q["options"], key=f"drill_{st.session_state.current_q_index}")
                show_hint = st.checkbox("Show Hint", key=f"drill_hint_{st.session_state.current_q_index}")
                if show_hint:
                    st.info(q.get("hint", "No hint available."))

                if st.button("Submit Answer", key=f"submit_drill_{st.session_state.current_q_index}"):
                    if choice == q["answer"]:
                        st.success("✅ Correct!")
                        st.session_state.scores[event] = st.session_state.scores.get(event, 0) + 1
                    else:
                        st.error(f"❌ Incorrect! Correct answer: {q['answer']}")
                    entry = f"Q{st.session_state.current_q_index + 1}: {q['question']} - Answer: {q['answer']}"
                    if entry not in st.session_state.selected_questions:
                        st.session_state.selected_questions.append(entry)

                    # Move to next question
                    st.session_state.current_q_index += 1
            else:
                st.success("🎉 You've answered all questions!")
