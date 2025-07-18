from abc import ABC, abstractmethod

class EvaluationStrategy(ABC):
    @abstractmethod
    def evaluate(self, user_answer, correct_answer) -> bool:
        pass

class MCQEvaluationStrategy(EvaluationStrategy):
    def evaluate(self, user_answer, correct_answer) -> bool:
        return user_answer == correct_answer
    
class FillBlankEvaluationStrategy(EvaluationStrategy):
    def evaluate(self, user_answer, correct_answer) -> bool:
        return user_answer.strip().lower() == correct_answer.strip().lower()