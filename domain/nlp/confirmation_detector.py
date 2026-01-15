from domain.nlp.pipeline import PipelineStep, StepResult
from domain.state.conversation_state import conversation_state


class ConfirmationDetector(PipelineStep):

    CONFIRM_WORDS = {
        "sim", "ok", "claro", "pode", "vai", "continua",
        "continue", "concordo", "perfeito", "isso mesmo",
        "pode continuar", "vamos", "manda ver", "faz isso"
    }

    def run(self, text: str, context: dict) -> StepResult:

        if not conversation_state.awaiting_confirmation():
            return StepResult(False)

        txt = text.lower().strip()

        if any(w in txt for w in self.CONFIRM_WORDS):
            action = conversation_state.current_step().get("action")
            conversation_state.advance_step()
            return StepResult(True, action)

        return StepResult(False)
