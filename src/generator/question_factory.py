from abc import ABC, abstractmethod
from src.models.questions_schema import Question, MCQuestion, FillBlankQuestion
from langchain.output_parsers import PydanticOutputParser
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException
from src.common.constants import BLANK

class QuestionFactory(ABC):
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self, prompt, parser, topic, difficulty):
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}")
                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty))
                parsed = parser.parse(response.content)
                self.logger.info("Successfully parsed question")
                return parsed
            except Exception as e:
                self.logger.error(f"Error: {str(e)}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise CustomException(f"Generator failed after {settings.MAX_RETRIES} attempts", e)
                
    @abstractmethod
    def create_question(self, topic: str, difficulty: str = 'medium') -> Question:
        pass

class MCQFactory(QuestionFactory):
    def create_question(self, topic:str, difficulty:str = 'medium') -> MCQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQuestion)
            question = self._retry_and_parse(mcq_prompt_template, parser, topic=topic, difficulty=difficulty)
            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ structure")
            
            self.logger.info("Generated a valid MCQ")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException("MCQ generation failed", e)
        
class FillBlankFactory(QuestionFactory):
    def create_question(self, topic:str, difficulty:str = 'medium') -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question = self._retry_and_parse(fill_blank_prompt_template, parser, topic=topic, difficulty=difficulty)
            if BLANK not in question.question:
                raise ValueError(f"Fill in blank questions should contrain {BLANK}")
            
            self.logger.info("Generated a valid Fill-in-blank question")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException("MCQ generation failed", e)

