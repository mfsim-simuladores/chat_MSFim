from domain.state.conversation_state import conversation_state
from domain.logging.sse_events import SSEEvent

YES = {"sim", "s", "pode", "quero", "vamos", "prosseguir", "simm"}
NO  = {"não", "nao", "n", "agora não", "prefiro não"}


class WizardHandler:
    def __init__(self, executor):
        self.state = conversation_state
        self.executor = executor

    def handle(self, text: str) -> bool:
        # Nenhum wizard ativo
        if not self.state.wizard_running():
            return False

        step = self.state.current_step()
        if not step:
            return False

        user = text.strip().lower()
        step_type = step.get("type")

        # ==================================================
        # CONFIRMATION (sim / não)
        # ==================================================
        if step_type == "confirmation":

            if user not in YES and user not in NO:
                return False

            # 🔥 PRIMEIRO "SIM" APENAS LIBERA O PASSO 1
            # Não executa ação, apenas avança e mostra a pergunta
            if self.state.just_started:
                self.state.just_started = False
                self._advance_and_show_next()
                return True

            # Executa ação SOMENTE do passo atual
            if user in YES:
                action = step.get("action")
                if action:
                    self.executor.execute(action)

            self._advance_and_show_next()
            return True

        # ==================================================
        # WAIT OK (apenas "ok")
        # ==================================================
        if step_type == "wait_ok":
            if user != "ok":
                return False

            self._advance_and_show_next()
            return True

        # ==================================================
        # FINAL
        # ==================================================
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

    # ==================================================
    # AVANÇA UM PASSO E MOSTRA A PERGUNTA DO PRÓXIMO
    # ==================================================
    def _advance_and_show_next(self):
        self.state.advance_step()
        next_step = self.state.current_step()

        if not next_step:
            return

        self.executor.feedback(
            SSEEvent.action(
                "Instalação",
                next_step["message"]
            )
        )
