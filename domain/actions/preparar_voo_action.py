from .base import Action

class PrepararVooAction(Action):
    action_name = "preparar_voo"

    def execute(self, executor):
        executor.checklist_pre_voo()
        return None

