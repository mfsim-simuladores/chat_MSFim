from .base import Action

class PrepararVooAction(Action):
    action_name = "preparar_voo"

    def execute(self, executor, payload=None):
        executor.checklist_pre_voo()
        return None

