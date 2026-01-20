from .base import Action

class DiagnosticarBussolaAction(Action):
    action_name = "diagnosticar_bussola"

    def execute(self, executor, payload=None):
        return executor.diagnosticar_bussola()