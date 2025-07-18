from typing import List
from pydantic import BaseModel, Field, validator
from abc import ABC


class Question(ABC, BaseModel):
    question: str = Field(description="The question text")

    @validator("question", pre=True)
    def extract_question_text_from_llm_response(cls, llm_response):
        if isinstance(llm_response, dict):
            return llm_response.get("description", str(llm_response))
        return str(llm_response)


class MCQuestion(Question):
    options: List[str] = Field(description="List of 4 questions")
    correct_answer: str = Field(description="The correct answer from the options")


class FillBlankQuestion(Question):
    answer: str = Field(description="The correct word or phrase for the blank")
