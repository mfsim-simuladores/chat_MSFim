from .base import Action

class CorrigirBussolaAction(Action):
    action_name = "corrigir_bussola"

    def execute(self, executor):
        return executor.executar_correcao_automatica()
