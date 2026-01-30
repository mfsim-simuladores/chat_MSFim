from domain.nlp.pipeline import PipelineStep, StepResult
from domain.learning.learning_service import LearningService

class LearningFallbackStep(PipelineStep):
    def __init__(self, learning_service):
        self.learning = learning_service

    def run(self, text, context):
        self.learning.registrar_instrucao(text)
        return StepResult(
            True,
            {
                "action": "responder_texto",
                "payload": "🤖 No momento não consigo responder, mas em breve estarei aprendendo mais!"
            }
        )

        