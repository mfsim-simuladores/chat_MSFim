from domain.nlp.pipeline import PipelineStep, StepResult


class ExactMatcher(PipelineStep):
    def __init__(self, knowledge_manager):
        self.km = knowledge_manager

    def run(self, text, context):
        item = self.km.find_exact(text)

        if not item:
            return StepResult(False)

        if item.action == "responder_texto":
            return StepResult(
                resolved=True,
                output=item.response
            )

        return StepResult(
            resolved=True,
            output={
                "action": item.action,
                "payload": item.response
            }
        )


