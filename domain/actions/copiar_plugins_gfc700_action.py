from .base import Action

class CopiarPluginsGFC700Action(Action):
    action_name = "copiar_plugins_gfc700"

    def execute(self, executor):
        return executor.copiar_plugins_gfc700()
