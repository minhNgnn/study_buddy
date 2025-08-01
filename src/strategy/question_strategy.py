from abc import ABC, abstractmethod
from src.generator.question_factory import QuestionFactory
import streamlit as st


class QuestionStrategy(ABC):
    @abstractmethod
    def generate(self, qtype: str, topic, difficulty):
        pass

    @abstractmethod
    def attempt(self, question, index):
        pass

    @abstractmethod
    def evaluate(self, user_answer, correct_answer) -> bool:
        pass


class MCQStrategy(QuestionStrategy):
    def generate(self, qtype, topic, difficulty):
        question = QuestionFactory.create(qtype, topic, difficulty)
        return {
            "type": "MCQ",
            "question": question.question,
            "options": question.options,
            "correct_answer": question.correct_answer,
            "strategy": self,
        }

    def attempt(self, question, index):
        return st.radio(
            f"Select an answer for Question {index + 1}",
            question["options"],
            key=f"mcq_{index}",
        )

    def evaluate(self, user_answer, correct_answer) -> bool:
        return user_answer == correct_answer


class FillBlankStrategy(QuestionStrategy):
    def generate(self, qtype, topic, difficulty):
        question = QuestionFactory.create(qtype, topic, difficulty)
        return {
            "type": "Fill in the blank",
            "question": question.question,
            "correct_answer": question.answer,
            "strategy": self,
        }

    def attempt(self, question, index):
        return st.text_input(
            f"Fill in the blank for Question {index + 1}", key=f"fill_blank_{index}"
        )

    def evaluate(self, user_answer, correct_answer) -> bool:
        return user_answer.strip().lower() == correct_answer.strip().lower()
