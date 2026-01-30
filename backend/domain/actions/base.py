class Action:
    action_name = None

    def execute(self, executor, *args, **kwargs):
        raise NotImplementedError("Ação não implementada.")