from .base import Action

class VerificarInstalacaoXPlaneAction(Action):
    action_name = "verificar_inxplane"

    def execute(self, executor):
        return executor.verificar_instalacao_xplane()