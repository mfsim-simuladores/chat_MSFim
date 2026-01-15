from .base import Action

class PluginsXPlaneAction(Action):
    action_name = "verinsta_pluginxplane"

    def execute(self, executor):
        return executor.plugins_xplane()