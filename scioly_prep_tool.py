# scioly_prep_tool.py
import streamlit as st
import random
import time
import json

# ------------------------------
# Load questions from JSON file
# ------------------------------
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

# Organize questions by event
questions_by_event = {}
for q in all_questions:
    event = q.get("event", "Unknown")
    questions_by_event.setdefault(event, []).append(q)

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
# Sidebar: Event & Mode
# ------------------------------
event = st.selectbox("Select Event:", list(questions_by_event.keys()))
mode = st.radio("Select Mode:", ["Study Mode", "Timed Drill"])

# ------------------------------
# Sidebar: Topic & Difficulty Filtering
# ------------------------------
topics = list(set(q.get('topic', 'Unknown') for q in questions_by_event[event]))
selected_topics = st.multiselect("Filter by Topic:", topics, default=topics)

difficulties = list(set(q.get('difficulty', 'Unknown') for q in questions_by_event[event]))
selected_difficulty = st.multiselect("Select Difficulty:", difficulties, default=difficulties)

# ------------------------------
# Filter questions based on selection
# ------------------------------
filtered_questions = [
    q for q in questions_by_event[event]
    if q.get('topic', 'Unknown') in selected_topics and q.get('difficulty', 'Unknown') in selected_difficulty
]
random.shuffle(filtered_questions)

# Display number of questions and recommended time
num_questions = len(filtered_questions)
recommended_time = num_questions  # 1 minute per question
st.markdown(f"**Number of questions selected:** {num_questions}")
st.markdown(f"**Recommended time:** {recommended_time} minutes (1 min per question)")

# ------------------------------
# Timed Drill Setup
# ------------------------------
if mode == "Timed Drill":
    time_limit = st.number_input(
        "Enter time limit (minutes):",
        min_value=1,
        value=recommended_time,
        help="Adjust time to challenge yourself or accept the recommended time."
    )

    start_drill = st.button("Start Timed Drill")
    
    if start_drill:
        start_time = time.time()
        total_seconds = time_limit * 60  # convert minutes to seconds
        
        for i, q in enumerate(filtered_questions, 1):
            elapsed = time.time() - start_time
            if elapsed > total_seconds:
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
# Display Scores / Progress Analytics
# ------------------------------
st.write("### Your Scores")
for e, score in st.session_state.scores.items():
    st.write(f"{e}: {score} correct answers")
