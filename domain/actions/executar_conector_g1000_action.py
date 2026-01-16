from .base import Action

class ExecutarConectorG1000Action(Action):
    action_name = "executar_conector_g1000"

    def execute(self, executor):
        return executor.executar_conector_g1000()
