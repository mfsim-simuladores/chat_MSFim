from .base import Action

class RespondeTextoAction (Action):
    action_name = "responder_texto"

    def execute(self, executor):
        return executor.responder_texto()