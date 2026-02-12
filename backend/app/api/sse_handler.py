import asyncio
import json
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from domain.logging.sse_events import SSEEvent
from domain.state.conversation_state import conversation_state
from domain.nlp.pipeline import PipelineStep
from domain.actions.registry import ACTIONS_REGISTRY

router = APIRouter(prefix="/sse")
END = "__END__"


async def event_generator(text, pipeline, executor):

    queue = asyncio.Queue()

    def feedback(ev):
        queue.put_nowait(ev)

    executor.set_feedback(feedback)

    context = {
        "executor": executor
    }

    queue.put_nowait(SSEEvent.action("Interpretando", ""))

    result = pipeline.interpret(text, context)


    if result is None:
        if "llm_response" in context:
            queue.put_nowait(
                SSEEvent.log(
                    context["llm_response"],
                    title="Assistente"
                )
            )
        else:
            queue.put_nowait(
                SSEEvent.error("Nenhuma ação", "Nada encontrado")
            )

        queue.put_nowait(END)
        return

    if isinstance(result, dict):
        action_name = result.get("action")
        payload = result.get("payload")
    else:
        action_name = result
        payload = None


    async def run():
        try:
            if not conversation_state.wizard_running():
                executor.execute(action_name, payload)

                if not conversation_state.awaiting_confirmation():
                    queue.put_nowait(
                        SSEEvent.finished(
                            "Concluído",
                            ""
                        )
                    )

        except Exception as e:
            queue.put_nowait(
                SSEEvent.error("Erro", str(e))
            )
        finally:
            queue.put_nowait(END)

    asyncio.create_task(run())

    while True:
        ev = await queue.get()
        if ev == END:
            break

        yield json.dumps(ev, ensure_ascii=False)





@router.get("/run")
async def sse_run_action(request: Request, text: str):

    pipeline = request.app.state.pipeline
    executor = request.app.state.executor

    return EventSourceResponse(
        event_generator(text, pipeline, executor)
    )