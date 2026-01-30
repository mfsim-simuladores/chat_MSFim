from .base import Action

class DiagnosticarMotorAction(Action):
    action_name = "diagnosticar_motor"

    def execute(self, executor, payload=None):
        return executor.diagnosticar_motor()