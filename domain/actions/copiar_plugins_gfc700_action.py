from .base import Action

class CopiarPluginsGFC700Action(Action):
    action_name = "copiar_plugins_gfc700"

    def execute(self, executor, payload=None):
        return executor.copiar_plugins_gfc700()
