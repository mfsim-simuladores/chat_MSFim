from .base import Action

class RespondeTextoAction(Action):
    action_name = "responder_texto"

    def execute(self, executor, payload=None):
        if isinstance(payload, str):
            return payload
        return ""

