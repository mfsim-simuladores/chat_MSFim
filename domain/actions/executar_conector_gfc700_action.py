from .base import Action

class ExecutarConectorGFC700Action(Action):
    action_name = "executar_conector_gfc700_csharp"

    def execute(self, executor):
        return executor.executar_conector_gfc700_csharp()
