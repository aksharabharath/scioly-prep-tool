# scioly_prep_tool.py
import streamlit as st
import json
import random
import time

# ------------------------------
# Load Questions from JSON
# ------------------------------
with open("all_questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# ------------------------------
# Streamlit App
# ------------------------------
st.title("Science Olympiad Prep Tool")

# Initialize session state
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'scores' not in st.session_state:
    st.session_state.scores = {}

# ------------------------------
# Sidebar / Filters
# ------------------------------
events = list(set(q['event'] for q in all_questions))
event = st.selectbox("Select Event:", events)

# Filter questions for the selected event
event_questions = [q for q in all_questions if q['event'] == event]

# Topics
topics = list(set(q['topic'] for q in event_questions))
selected_topics = st.multiselect("Filter by Topic:", topics, default=topics)

# Difficulty
difficulties = list(set(q['difficulty'] for q in event_questions))
selected_difficulty = st.multiselect("Select Difficulty:", difficulties, default=difficulties)

# Filter questions based on selected topics and difficulty
filtered_questions = [q for q in event_questions if q['topic'] in selected_topics and q['difficulty'] in selected_difficulty]
random.shuffle(filtered_questions)

# ------------------------------
# Mode Selection
# ------------------------------
mode = st.radio("Select Mode:", ["Study Mode", "Timed Drill"])

# ------------------------------
# Timed Drill
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
                st.info(q["hint"])
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
# Study Mode
# ------------------------------
else:
    for i, q in enumerate(filtered_questions, 1):
        st.write(f"**Q{i}: {q['question']}**")
        choice = st.radio("Select answer:", q["options"], key=f"{event}_{i}")
        show_hint = st.checkbox("Show Hint", key=f"hint_{i}")
        if show_hint:
            st.info(q["hint"])
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

# ------------------------------
# Reset Progress
# ------------------------------
if st.button("Reset Progress"):
    st.session_state.selected_questions = []
    st.session_state.scores[event] = 0
    st.success("Progress reset!")

# ------------------------------
# Display Scores
# ------------------------------
st.write("### Your Scores")
for e, score in st.session_state.scores.items():
    st.write(f"{e}: {score} correct answers")
