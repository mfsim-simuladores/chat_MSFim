from domain.nlp.pipeline import PipelineStep, StepResult

class SemanticStep(PipelineStep):
    def __init__(self, semantic_search, knowledge_manager, threshold=0.5):
        self.search = semantic_search
        self.km = knowledge_manager
        self.threshold = threshold

    def run(self, text, context):
        item = self.search.buscar(text)
        if not item:
            return StepResult(False)

        if isinstance(item, dict):
            action = item.get("Action") or item.get("action")
        else:
            action = getattr(item, "action", None)

        if not isinstance(action, str):
            return StepResult(False)

        return StepResult(True, action)
