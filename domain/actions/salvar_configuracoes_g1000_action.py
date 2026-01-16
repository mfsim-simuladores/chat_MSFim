from .base import Action

class salvarConfiguracoes(Action):
    action_name = "salvar_configuracoes_g1000"

    def execute(self, executor):
        return executor.salvar_configuracoes_g1000()
