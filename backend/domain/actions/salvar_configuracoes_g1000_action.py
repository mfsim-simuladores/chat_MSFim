from .base import Action

class salvarConfiguracoes(Action):
    action_name = "salvar_configuracoes_g1000"

    def execute(self, executor, payload=None):
        return executor.salvar_configuracoes_g1000()
