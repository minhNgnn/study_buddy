from src.models.questions_schema import Question, MCQuestion, FillBlankQuestion
from langchain.output_parsers import PydanticOutputParser
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException
from src.common.constants import BLANK


class QuestionFactory:
    llm = get_groq_llm()
    logger = get_logger("QuestionFactory")

    @classmethod
    def _retry_and_parse(cls, prompt, parser, topic, difficulty):
        for attempt in range(settings.MAX_RETRIES):
            try:
                cls.logger.info(
                    f"Generating question for topic {topic} with difficulty {difficulty}"
                )
                response = cls.llm.invoke(
                    prompt.format(topic=topic, difficulty=difficulty)
                )
                parsed = parser.parse(response.content)
                cls.logger.info("Successfully parsed question")
                return parsed
            except Exception as e:
                cls.logger.error(f"Error: {str(e)}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise CustomException(
                        f"Generator failed after {settings.MAX_RETRIES} attempts", e
                    )

    @classmethod
    def create(cls, qtype: str, topic: str, difficulty: str = "medium") -> Question:
        try:
            if qtype == "mcq":
                parser = PydanticOutputParser(pydantic_object=MCQuestion)
                question = cls._retry_and_parse(
                    mcq_prompt_template, parser, topic, difficulty
                )
                if (
                    len(question.options) != 4
                    or question.correct_answer not in question.options
                ):
                    raise ValueError("Invalid MCQ structure")
                cls.logger.info("Generated a valid MCQ")
                return question

            elif qtype == "fillblank":
                parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
                question = cls._retry_and_parse(
                    fill_blank_prompt_template, parser, topic, difficulty
                )
                if BLANK not in question.question:
                    raise ValueError(
                        f"Fill-in-the-blank questions must contain {BLANK}"
                    )
                cls.logger.info("Generated a valid Fill-in-the-blank question")
                return question

            else:
                raise ValueError(f"Unsupported question type: {qtype}")

        except Exception as e:
            cls.logger.error(f"Failed to generate question of type {qtype}: {str(e)}")
            raise CustomException(f"{qtype} generation failed", e)
