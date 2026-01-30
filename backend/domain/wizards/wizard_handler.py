from domain.state.conversation_state import conversation_state
from domain.logging.sse_events import SSEEvent

YES = {"sim", "s", "pode", "quero", "vamos", "prosseguir", "simm"}
NO  = {"não", "nao", "n", "agora não", "prefiro não"}
BACK = {
    "voltar",
    "anterior",
    "passo anterior",
    "back"
}

CANCEL = {
    "cancelar",
    "parar",
    "sair",
    "abortar",
    "encerrar"
}


class WizardHandler:
    def __init__(self, executor):
        self.state = conversation_state
        self.executor = executor

    def handle(self, text: str) -> bool:
        if not self.state.wizard_running():
            return False
        user = text.strip().lower()

        step = self.state.current_step()
        if not step:
            return False

        step_type = step["type"]

        #  COMANDO GLOBAL: VOLTAR UM PASSO
        if user in BACK:
            if self.state.can_go_back():
                self.state.go_back()
                step = self.state.current_step()

                self.executor.feedback(
                    SSEEvent.message(
                        title="⬅ Passo anterior",
                        message=step["message"],
                        attachments=step.get("attachments"),
                        media=step.get("media"),
                    )
                )
            else:
                self.executor.feedback(
                    SSEEvent.log("Você já está no primeiro passo do assistente.")
                )
            return True

        
        #  COMANDO GLOBAL: CANCELAR WIZARD
        if user in CANCEL:
            self.state.stop_wizard()

            self.executor.feedback(
                SSEEvent.warning(
                    title="Assistente cancelado",
                    message="O assistente foi interrompido. Caso queira recomeçar, é só avisar."
                )
            )
            return True

        #  COMANDO "manual" (APENAS EM wait_ok)
        
        if step_type == "wait_ok" and user == "manual":
            attachments = step.get("attachments")

            if attachments:
                self.executor.feedback(
                    SSEEvent.message(
                        title="📄 Manual",
                        message="Manual disponível para consulta:",
                        attachments=attachments
                    )
                )
            else:
                self.executor.feedback(
                    SSEEvent.log("Nenhum manual disponível neste passo.")
                )
            return True

        #  PERGUNTA LIVRE DURANTE WIZARD (NÃO QUEBRA O FLUXO)
        if step_type in {"wait_ok", "confirmation"}:
            comandos_wizard = (
                {"ok"} |
                YES |
                NO |
                BACK |
                CANCEL |
                {"manual"}
            )

            if user not in comandos_wizard:
                return False


        # WAIT_OK
        if step_type == "wait_ok":
            if user != "ok":
                return True

            self.state.advance_step()
            next_step = self.state.current_step()
            if not next_step:
                return True

            self.executor.feedback(
                SSEEvent.message(
                    title=next_step.get("title", "Instalação"),
                    message=next_step["message"],
                    attachments=next_step.get("attachments"),
                    media=next_step.get("media"),
                )
            )
            return True

        # CONFIRMATION
        if step_type == "confirmation":
            if user not in YES and user not in NO:
                return False

            if user in YES and "action" in step:
                self.executor.execute(step["action"])

            self.state.advance_step()
            next_step = self.state.current_step()
            if not next_step:
                return True

            self.executor.feedback(
                SSEEvent.message(
                    title=next_step.get("title", "Instalação"),
                    message=next_step["message"],
                    attachments=next_step.get("attachments"),
                    media=next_step.get("media"),
                )
            )
            return True

        # ======================================================
        # 🏁 FINAL
        # ======================================================
        if step_type == "final":
            self.executor.feedback(
                SSEEvent.message(
                    title="Instalação concluída",
                    message=step["message"],
                    attachments=step.get("attachments"),
                    media=step.get("media"),
                )
            )
            self.state.advance_step()
            return True

        return False
