from .base import Action

class FixarGFC700TaskbarAction(Action):
    action_name = "fixar_gfc700_taskbar_csharp"

    def execute(self, executor, payload=None):
        return executor.fixar_gfc700_taskbar_csharp()
