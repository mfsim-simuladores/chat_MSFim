from .base import Action

class CopiarArquivosG1000Action(Action):
    action_name = "copiar_arquivos_joystick_g1000"

    def execute(self, executor):
        return executor.copiar_arquivos_joystick_g1000()
