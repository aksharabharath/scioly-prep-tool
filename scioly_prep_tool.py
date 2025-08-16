# scioly_prep_tool.py
import streamlit as st
import random
import time
import json

# ------------------------------
# Load Questions from JSON
# ------------------------------
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Organize questions by event
questions_by_event = {}
for q in all_questions:
    event_name = q.get("event", "Unknown")
    questions_by_event.setdefault(event_name, []).append(q)

# ------------------------------
# Streamlit App
# ------------------------------
st.title("Science Olympiad Prep Tool")

# Initialize session state
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'drill_active' not in st.session_state:
    st.session_state.drill_active = False
if 'drill_start_time' not in st.session_state:
    st.session_state.drill_start_time = 0
if 'time_limit' not in st.session_state:
    st.session_state.time_limit = 60

# Sidebar options
event = st.selectbox("Select Event:", list(questions_by_event.keys()))
mode = st.radio("Select Mode:", ["Study Mode", "Timed Drill"])

# Topic Filtering
topics = list(set(q.get('topic', 'Unknown') for q in questions_by_event[event]))
selected_topics = st.multiselect("Filter by Topic:", topics, default=topics)

# Difficulty Filtering
difficulties = list(set(q.get('difficulty', 'Easy') for q in questions_by_event[event]))
selected_difficulty = st.multiselect("Select Difficulty:", difficulties, default=difficulties)

# Filter questions based on selection
filtered_questions = [q for q in questions_by_event[event] 
                      if q.get('topic', 'Unknown') in selected_topics and q.get('difficulty', 'Easy') in selected_difficulty]
random.shuffle(filtered_questions)

# ------------------------------
# Timed Drill Mode
# ------------------------------
if mode == "Timed Drill":
    st.session_state.time_limit = st.number_input("Enter time limit in seconds:", min_value=30, value=60, key="time_limit_input")
    if not st.session_state.drill_active:
        if st.button("Start Timed Drill", key="start_drill_button"):
            st.session_state.drill_active = True
            st.session_state.drill_start_time = time.time()
            st.session_state.current_q_index = 0

    if st.session_state.drill_active:
        elapsed = time.time() - st.session_state.drill_start_time
        if elapsed > st.session_state.time_limit:
            st.warning("Time's up!")
            st.session_state.drill_active = False
        elif st.session_state.current_q_index < len(filtered_questions):
            q = filtered_questions[st.session_state.current_q_index]
            st.write(f"**Q{st.session_state.current_q_index + 1}: {q['question']}**")
            choice = st.radio("Select answer:", q["options"], key=f"drill_radio_{st.session_state.current_q_index}")
            show_hint = st.checkbox("Show Hint", key=f"drill_hint_{st.session_state.current_q_index}")
            if show_hint:
                st.info(q.get("hint", "No hint available."))
            
            if st.button("Submit Answer", key=f"submit_drill_{st.session_state.current_q_index}"):
                if choice == q["answer"]:
                    st.success("Correct!")
                    st.session_state.scores[event] = st.session_state.scores.get(event, 0) + 1
                else:
                    st.error(f"Incorrect! Correct answer: {q['answer']}")
                entry = f"Q{st.session_state.current_q_index + 1}: {q['question']} - Answer: {q['answer']}"
                if entry not in st.session_state.selected_questions:
                    st.session_state.selected_questions.append(entry)
                st.session_state.current_q_index += 1
        else:
            st.info("All questions completed!")
            st.session_state.drill_active = False

# ------------------------------
# Study Mode
# ------------------------------
else:
    for i, q in enumerate(filtered_questions, 1):
        st.write(f"**Q{i}: {q['question']}**")
        choice = st.radio("Select answer:", q["options"], key=f"study_radio_{i}")
        show_hint = st.checkbox("Show Hint", key=f"study_hint_{i}")
        if show_hint:
            st.info(q.get("hint", "No hint available."))
        if st.button(f"Submit Q{i}", key=f"submit_study_{i}"):
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
if st.button("Generate Cheat Sheet", key="generate_cheat_sheet"):
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
if st.button("Reset Progress", key="reset_progress"):
    st.session_state.selected_questions = []
    st.session_state.scores[event] = 0
    st.session_state.current_q_index = 0
    st.session_state.drill_active = False
    st.success("Progress reset!")

# ------------------------------
# Display Scores
# ------------------------------
st.write("### Your Scores")
for e, score in st.session_state.scores.items():
    st.write(f"{e}: {score} correct answers")
