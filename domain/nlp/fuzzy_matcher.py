from domain.nlp.pipeline import PipelineStep, StepResult
from rapidfuzz import fuzz

class FuzzyMatcher(PipelineStep):
    def __init__(self, knowledge_manager, threshold=55):
        self.km = knowledge_manager
        self.threshold = threshold

    def run(self, text, context):
        best_item = None
        best_score = 0

        for item in self.km.all_items():
            score = fuzz.token_set_ratio(
                text.lower(),
                item.question.lower()
            )

            if score > best_score:
                best_item = item
                best_score = score

        if best_item and best_score >= self.threshold:
            return StepResult(
                True,
                {
                    "action": best_item.action,
                    "payload": best_item.response
                }
            )


        return StepResult(False)
