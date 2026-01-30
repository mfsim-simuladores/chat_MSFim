class StepResult:
    def __init__(self, resolved: bool, output=None, stop: bool = False):
        self.resolved = resolved
        self.output = output
        self.stop = stop


class PipelineStep:
    def run(self, text: str, context: dict) -> StepResult:
        raise NotImplementedError


class InterpreterPipeline:
    def __init__(self, steps):
        self.steps = steps

    def interpret(self, text: str, context=None):
        if context is None:
            context = {}

        for step in self.steps:
            result = step.run(text, context)

            if not isinstance(result, StepResult):
                raise RuntimeError(
                    f"Step '{step.__class__.__name__}' retornou objeto inválido."
                )

            if result.resolved:
                if result.stop:
                    return None
                if result.output:
                    return result.output

        return None