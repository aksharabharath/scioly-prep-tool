# scioly_prep_tool.py
import streamlit as st

# ------------------------------
# Sample Questions per Event
# ------------------------------
questions = {
    "Astronomy": [
        {
            "question": "Which is the brightest star in the night sky?",
            "options": ["Sirius", "Betelgeuse", "Rigel", "Vega"],
            "answer": "Sirius"
        },
        {
            "question": "The H-R diagram plots which two properties?",
            "options": ["Mass vs Temperature", "Luminosity vs Temperature", "Distance vs Brightness", "Radius vs Mass"],
            "answer": "Luminosity vs Temperature"
        }
    ],
    "Forensics": [
        {
            "question": "Which technique separates DNA fragments?",
            "options": ["Chromatography", "Electrophoresis", "Spectroscopy", "Centrifugation"],
            "answer": "Electrophoresis"
        },
        {
            "question": "Fingerprints are classified into how many main types?",
            "options": ["2", "3", "4", "5"],
            "answer": "3"
        }
    ],
    "Circuit Lab": [
        {
            "question": "Ohm's Law formula is?",
            "options": ["V=IR", "P=VI", "V=I^2R", "E=mc^2"],
            "answer": "V=IR"
        },
        {
            "question": "Resistors in series have which total resistance?",
            "options": ["Sum of resistances", "Reciprocal sum", "Maximum resistance", "Minimum resistance"],
            "answer": "Sum of resistances"
        }
    ],
    "Remote Sensing": [
        {
            "question": "Which part of EM spectrum is used for thermal imaging?",
            "options": ["Infrared", "Visible", "UV", "Microwave"],
            "answer": "Infrared"
        },
        {
            "question": "Which satellite provides daily images for climate monitoring?",
            "options": ["GOES", "Hubble", "Chandra", "Kepler"],
            "answer": "GOES"
        }
    ]
}

# ------------------------------
# Streamlit App
# ------------------------------
st.title("Science Olympiad Prep Tool")

# Event Selection
event = st.selectbox("Select Event:", list(questions.keys()))

st.write(f"### {event} Drill")

# Question Loop
selected_questions = []  # For cheat sheet
for i, q in enumerate(questions[event], 1):
    st.write(f"**Q{i}: {q['question']}**")
    choice = st.radio("Select answer:", q["options"], key=f"{event}_{i}")
    
    if st.button(f"Submit Q{i}", key=f"submit_{event}_{i}"):
        if choice == q["answer"]:
            st.success("Correct!")
        else:
            st.error(f"Incorrect! Correct answer: {q['answer']}")
        selected_questions.append(f"Q{i}: {q['question']} - Answer: {q['answer']}")

# Cheat Sheet Generator
if st.button("Generate Cheat Sheet"):
    if selected_questions:
        cheat_text = "\n".join(selected_questions)
        st.write("### Cheat Sheet")
        st.text(cheat_text)
        st.download_button("Download Cheat Sheet", cheat_text, file_name=f"{event}_cheatsheet.txt")
    else:
        st.warning("No questions answered yet!")
