from domain.nlp.pipeline import PipelineStep, StepResult
from domain.state.conversation_state import conversation_state


class ConfirmationDetector(PipelineStep):

    CONFIRM_WORDS = {
        "sim", "ok", "claro", "pode", "vai", "continua",
        "continue", "concordo", "perfeito", "isso mesmo",
        "pode continuar", "vamos", "manda ver", "faz isso"
    }

    CANCEL_WORDS = {
        "não", "nao", "n", "cancela", "cancelar", "pare", "para"
    }

    def run(self, text: str, context: dict) -> StepResult:

        if not conversation_state.awaiting_confirmation():
            return StepResult(False)

        txt = text.lower().strip()

        if any(w in txt for w in self.CONFIRM_WORDS):
            action = conversation_state.consume_confirmation()
            return StepResult(True, action)

        if any(w in txt for w in self.CANCEL_WORDS):
            conversation_state.reset()
            return StepResult(
                True,
                {
                    "action": None,
                    "message": "Operação cancelada."
                },
                stop=True
            )

        return StepResult(False)
