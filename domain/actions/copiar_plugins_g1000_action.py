from .base import Action

class CopiarPluginsG1000Action(Action):
    action_name = "copiar_plugins_g1000"

    def execute(self, executor):
        return executor.copiar_plugins_g1000()
