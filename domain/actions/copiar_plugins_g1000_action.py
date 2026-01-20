from .base import Action

class CopiarPluginsG1000Action(Action):
    action_name = "copiar_plugins_g1000"

    def execute(self, executor, payload=None):
        return executor.copiar_plugins_g1000()
