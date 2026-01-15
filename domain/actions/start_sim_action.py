from .base import Action

class StartSimAction(Action):
    action_name = "start_sim"

    def execute(self, executor):
        return executor.abrir_xplane()