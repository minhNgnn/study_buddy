from typing import List
from pydantic import BaseModel, Field, validator

class MCQuestion(BaseModel):

    question: str = Field(description="The question text")
    option: List[str] = Field(description="List of 4 questions")
    correct_answer : str = Field(description="The correct answer from the options")

    @validator('question', pre=True)
    def extract_question_text_from_llm_response(cls, llm_response):
        if isinstance(llm_response, dict):
            return llm_response.get('description', str(llm_response))
        return str(llm_response)

class FillBlankQuestion(BaseModel):
    question: str = Field(description="The question text with '_____' for the blank")
    answer: str = Field(description="The correct word or phrase for the blank")

    @validator('question', pre=True)
    def extract_question_text_from_llm_response(cls, llm_response):
        if isinstance(llm_response, dict):
            return llm_response.get('description', str(llm_response))
        return str(llm_response)