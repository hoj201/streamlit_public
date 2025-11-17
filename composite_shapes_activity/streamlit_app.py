import streamlit as st
import pandas as pd
import random
import logging

from pathlib import Path
logger = st.logger.get_logger(__name__)
logger.setLevel(logging.INFO)
logger.info('Streamlit app started')

SCRIPT_DIR = Path(__file__).resolve().parent

answer_key = pd.read_csv(f"{SCRIPT_DIR}/fixtures/answer_key.csv", index_col="Question", dtype={"Answer": float})
with open(f"{SCRIPT_DIR}/fixtures/success_images.txt") as f:
    success_images = f.read().splitlines()

st.title("Composite shapes")
with open(f"{SCRIPT_DIR}/fixtures/directions.md") as f:
    directions = f.read()
st.markdown(directions)
st.latex(r"\pi \approx 3.14")
st.write("Area of a rectangle: length × width")
st.write("Area of a triangle: ½ × base × height")
st.write("Area of a circle: π × radius²")

st.header("Check your answers")
team_name = st.text_input("Team name", value="", max_chars=20, key="team_name_input")
if team_name not in st.session_state:
    st.session_state[team_name] = set()

selected_question = st.text_input("Question", value="", max_chars=1, key="question_select").upper()
if selected_question not in answer_key.index.get_level_values("Question"):
    st.error("Please enter a valid question. Available questions are: " + ", ".join(answer_key.index.get_level_values("Question")))

submitted_answer = st.text_input("Your answer", value="0", key="answer_input")

try:
    submitted_answer = float(submitted_answer)
except ValueError:
    st.error("Please enter a valid number for your answer. Round to two decimal places. For example, enter 12.34.")

if st.button("Check answer"):
    correct_answer = answer_key.loc[selected_question]["Answer"]
    if abs(submitted_answer - correct_answer) < 0.05:
        random.seed(selected_question)
        gif_url = random.choice(success_images)
        st.image(gif_url)
        st.text("Correct!  Swap roles and ask Mr. Jacobs or Mrs. Finan for another card.")
        st.session_state[team_name].add(selected_question)
    elif abs(submitted_answer - correct_answer) < 0.2:
        st.text(f"Almost! {submitted_answer} is very close. Make sure you rounded correctly and try again.")
    else:
        st.text(f"Sorry, {submitted_answer} is not correct. try again")

st.header("Team Score")
if team_name in st.session_state:
    st.write(f"Team {team_name} has {len(st.session_state[team_name])} correct answers.")