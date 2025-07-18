import os
import streamlit as st
import pandas as pd
from src.generator.question_factory import QuestionFactory
from src.strategy.question_strategy import QuestionStrategy

def rerun():
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)

class QuizManager:
    def __init__(self):
        self.questions = []
        self.user_answers = []
        self.results = []

    def generate_questions(self, factory: QuestionFactory, strategy: QuestionStrategy, topic: str, difficulty: str, num_questions: int):
        self.questions = []
        self.user_answers = []
        self.results = []

        try:
            for _ in range(num_questions):
                q = strategy.generate(factory, topic, difficulty.lower())
                self.questions.append(q)
        except Exception as e:
            st.error(f"Error generating question {e}")
            return False
        return True

    def attempt_quiz(self):
        for i, q in enumerate(self.questions):
            st.markdown(f"**Question {i+1} : {q['question']}**")
            user_answer = q['strategy'].attempt(q, i)
            self.user_answers.append(user_answer)

    def evaluate_quiz(self):
        self.results = []
        for i, (q, user_ans) in enumerate(zip(self.questions, self.user_answers)):
            result_dict = {
                'question_number': i + 1,
                'question': q['question'],
                'question_type': q["type"],
                'user_answer': user_ans,
                'correct_answer': q["correct_answer"],
                'options': q.get('options', []),
                "is_correct": q['strategy'].evaluate(user_ans, q["correct_answer"])
            }
            self.results.append(result_dict)

    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)

    def save_to_csv(self, filename_prefix="quiz_results"):
        if not self.results:
            st.warning("No results to save !!")
            return None
        df = self.generate_result_dataframe()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{filename_prefix}_{timestamp}.csv"
        os.makedirs('results', exist_ok=True)
        full_path = os.path.join('results', unique_filename)
        try:
            df.to_csv(full_path, index=False)
            st.success("Results saved sucesfully....")
            return full_path
        except Exception as e:
            st.error(f"Failed to save results {e}")
            return None

