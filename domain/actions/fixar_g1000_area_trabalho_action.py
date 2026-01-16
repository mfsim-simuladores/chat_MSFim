from .base import Action

class fixar_g1000_area_trabalho(Action):
    action_name = "fixar_g1000_area_trabalho"

    def execute(self, executor):
        return executor.fixar_g1000_area_trabalho()
