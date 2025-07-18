import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import QuizManager
from src.generator.question_factory import QuestionFactory
from src.strategy.question_strategy import MCQStrategy, FillBlankStrategy

load_dotenv()


def show_quiz_settings():
    st.sidebar.header("Quiz Settings")
    question_type = st.sidebar.selectbox(
        "Select Question Type", ["Multiple Choice", "Fill in the Blank"], index=0
    )
    topic = st.sidebar.text_input(
        "Ennter Topic", placeholder="Indian History, geography"
    )
    difficulty = st.sidebar.selectbox(
        "Dificulty Level", ["Easy", "Medium", "Hard"], index=1
    )
    num_questions = st.sidebar.number_input(
        "Number of Questions", min_value=1, max_value=10, value=5
    )
    return question_type, topic, difficulty, num_questions


def show_quiz():
    st.header("Quiz")
    st.session_state.quiz_manager.attempt_quiz()
    if st.button("Submit Quiz"):
        st.session_state.quiz_manager.evaluate_quiz()
        st.session_state.quiz_submitted = True
        rerun()


def show_results():
    st.header("Quiz Results")
    results_df = st.session_state.quiz_manager.generate_result_dataframe()
    if not results_df.empty:
        correct_count = results_df["is_correct"].sum()
        total_questions = len(results_df)
        score_percentage = (correct_count / total_questions) * 100
        st.write(f"Score : {score_percentage}")
        for _, result in results_df.iterrows():
            question_num = result["question_number"]
            if result["is_correct"]:
                st.success(f"✅ Question {question_num} : {result['question']}")
            else:
                st.error(f"❌ Question {question_num} : {result['question']}")
                st.write(f"Your answer : {result['user_answer']}")
                st.write(f"Correct answer : {result['correct_answer']}")
            st.markdown("-------")
        if st.button("Save Results"):
            saved_file = st.session_state.quiz_manager.save_to_csv()
            if saved_file:
                with open(saved_file, "rb") as f:
                    st.download_button(
                        label="Downlaod Results",
                        data=f.read(),
                        file_name=os.path.basename(saved_file),
                        mime="text/csv",
                    )
            else:
                st.warning("No results avialble")


def main():
    st.set_page_config(page_title="Study Buddy", page_icon="🎧🎧")
    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "rerun_trigger" not in st.session_state:
        st.session_state.rerun_trigger = False
    st.title("Study Buddy AI")
    question_type, topic, difficulty, num_questions = show_quiz_settings()
    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False
        factory = QuestionFactory()
        if question_type == "Multiple Choice":
            strategy = MCQStrategy()
        else:
            strategy = FillBlankStrategy()
        succces = st.session_state.quiz_manager.generate_questions(
            factory, strategy, topic, difficulty, num_questions
        )
        st.session_state.quiz_generated = succces
        rerun()
    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        show_quiz()
    if st.session_state.quiz_submitted:
        show_results()


def rerun():
    st.session_state["rerun_trigger"] = not st.session_state.get("rerun_trigger", False)


if __name__ == "__main__":
    main()
