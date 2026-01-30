from .base import Action

class StartSimAction(Action):
    action_name = "start_sim"

    def execute(self, executor, payload=None):
        return executor.abrir_xplane()