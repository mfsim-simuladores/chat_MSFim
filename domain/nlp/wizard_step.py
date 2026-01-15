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

        if conversation_state.wizard_running():
            step = conversation_state.current_step()

            if not step.get("_shown"):
                executor.feedback(
                SSEEvent.action(
                    context.get("wizard_title", "Instalação"),
                    step["message"]
                )
            )
            step["_shown"] = True
            return StepResult(True)

        handled = handler.handle(text)
        return StepResult(handled)

        for wizard in WIZARD_REGISTRY:
            for trigger in wizard["trigger"]:
                if trigger in lowered:
                    conversation_state.start_wizard(wizard)

                    step = conversation_state.current_step()

                    executor.feedback(
                        SSEEvent.action(
                            wizard["title"],
                            step["message"]
                        )
                    )

                    if step["type"] == "confirmation":
                        conversation_state.expect_confirmation()
                    elif step ["type"] == "wait_ok":
                        conversation_state.expect_ok()

                    return StepResult(True)

        return StepResult(False)
