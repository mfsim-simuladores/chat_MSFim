from domain.nlp.pipeline import PipelineStep, StepResult


class ExactMatcher(PipelineStep):
    def __init__(self, knowledge_manager):
        self.km = knowledge_manager

    def run(self, text, context):
        item = self.km.find_exact(text)

        if not item:
            return StepResult(False)

        return StepResult(True, item.action)
