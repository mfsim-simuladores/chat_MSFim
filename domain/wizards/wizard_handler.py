from domain.state.conversation_state import conversation_state
from domain.logging.sse_events import SSEEvent

YES = {"sim", "s", "pode", "quero", "vamos", "prosseguir", "simm"}
NO  = {"não", "nao", "n", "agora não", "prefiro não"}


class WizardHandler:
    def __init__(self, executor):
        self.state = conversation_state
        self.executor = executor

    def handle(self, text: str) -> bool:
        if not self.state.wizard_running():
            return False

        step = self.state.current_step()
        if not step:
            return False

        user = text.strip().lower()
        step_type = step["type"]

        # ============================
        # CONFIRMATION
        # ============================
        if step_type == "confirmation":

            if user not in YES and user not in NO:
                return False

            # 👉 EXECUTA AÇÃO APENAS DO PASSO ATUAL
            if user in YES and "action" in step:
                self.executor.execute(step["action"])

            # 👉 AVANÇA APENAS UM PASSO
            self.state.advance_step()

            next_step = self.state.current_step()
            if not next_step:
                return True

            # 👉 MOSTRA A PRÓXIMA PERGUNTA
            self.executor.feedback(
                SSEEvent.action(
                    "Instalação",
                    next_step["message"]
                )
            )
            return True

        # ============================
        # WAIT OK
        # ============================
        if step_type == "wait_ok":

            if user != "ok":
                return False

            self.state.advance_step()
            next_step = self.state.current_step()
            if not next_step:
                return True

            self.executor.feedback(
                SSEEvent.action(
                    "Instalação",
                    next_step["message"]
                )
            )
            return True

        # ============================
        # FINAL
        # ============================
        if step_type == "final":
            self.executor.feedback(
                SSEEvent.action(
                    "Instalação",
                    step["message"]
                )
            )
            self.state.advance_step()
            return True

        return False