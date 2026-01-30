from domain.nlp.pipeline import PipelineStep, StepResult
from domain.state.conversation_state import conversation_state
from domain.wizards.wizard_handler import WizardHandler
from domain.logging.sse_events import SSEEvent
from domain.wizards.wizard_registry import WIZARD_REGISTRY

class WizardStep(PipelineStep):

    def run(self, text: str, context: dict) -> StepResult:
        executor = context.get("executor")
        handler = WizardHandler(executor)

        # WIZARD ATIVO
        if conversation_state.wizard_running():
            handled = handler.handle(text)

            if handled:
                # Wizard tratou (ok, voltar, cancelar, etc)
                return StepResult(True)

            # ❗ NÃO TRATOU → deixa o pipeline continuar (Gemini, intents, etc)
            return StepResult(False)

        # INÍCIO DE WIZARD
        lowered = text.lower()
        for wizard in WIZARD_REGISTRY:
            for trigger in wizard["trigger"]:
                if trigger in lowered:
                    conversation_state.start_wizard(wizard)
                    step = conversation_state.current_step()

                    executor.feedback(
                        SSEEvent.message(
                            title=wizard.get("title", "Instalação"),
                            message=step["message"],
                            attachments=step.get("attachments"),
                            media=step.get("media"),
                        )
                    )
                    return StepResult(True)

        return StepResult(False)

