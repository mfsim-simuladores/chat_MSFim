from .base import Action

class CorrigirPreVooAction(Action):
    action_name = "corrigir_prevoo"

    def execute(self, executor, payload=None):
        return executor.executar_correcao_automatica()
