from domain.nlp.pipeline import PipelineStep, StepResult
from domain.state.conversation_state import conversation_state
from domain.wizards.wizard_handler import WizardHandler
from domain.logging.sse_events import SSEEvent
from domain.wizards.wizard_registry import WIZARD_REGISTRY


class WizardStep(PipelineStep):

    def run(self, text: str, context: dict) -> StepResult:
        executor = context.get("executor")
        handler = WizardHandler(executor)
        lowered = text.lower()

        # ======================================
        # SE UM WIZARD JÁ ESTÁ EM EXECUÇÃO
        # ======================================
        if conversation_state.wizard_running():
            handled = handler.handle(text)
            return StepResult(handled)

        # ======================================
        # INICIAR UM NOVO WIZARD
        # ======================================
        for wizard in WIZARD_REGISTRY:
            for trigger in wizard["trigger"]:
                if trigger in lowered:

                    conversation_state.start_wizard(wizard)
                    step = conversation_state.current_step()

                    executor.feedback(
                        SSEEvent.action(
                            wizard.get("title", "Instalação"),
                            step["message"]
                        )
                    )

                    return StepResult(True)

        # ======================================
        # NÃO FOI WIZARD
        # ======================================
        return StepResult(False)