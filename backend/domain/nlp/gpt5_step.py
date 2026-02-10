import os
from dotenv import load_dotenv
from openai import OpenAI
from domain.logging.sse_events import SSEEvent
from domain.nlp.pipeline import PipelineStep, StepResult
from domain.state.conversation_state import conversation_state

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    

class GPT5Connector:
    SYSTEM_PROMPT = """
Você é um assistente especializado em:
- Simuladores de voo
- Aviação geral
- X-plane 11 e 12
- Instrumentos Garmin (G1000, GNS, GFC, BARON...)
- Operação e sistemas de aeronaves

Responda perguntas informativas e tecnicas de forma clara, técnica, extremamente curta, use no máximo 3 frases curtas e objetiva."""

    MODEL = "gpt-5-mini"  
    @staticmethod
    def responder(prompt: str) -> str | None:
        try:
            response = client.responses.create(
                model=GPT5Connector.MODEL,
                input=[
                    {
                        "role": "system",
                        "content": GPT5Connector.SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_output_tokens=150   
            )

            return response.output_text.strip()

        except Exception as e:
            print("[GPT5Connector] Erro:", e)
            return None


class GPT5Step(PipelineStep):

    def run(self, text: str, context: dict) -> StepResult:

        if conversation_state.wizard_running():
            return StepResult(False)

        if not os.getenv("OPENAI_API_KEY"):
            return StepResult(False)

        resposta = GPT5Connector.responder(text)
        if not resposta:
            return StepResult(False, "GPT5_UNAVAILABLE")

        executor = context.get("executor")
        if executor:
            executor.feedback(
                SSEEvent.message(
                    title="Resposta",
                    message=resposta
                )
            )

        learning_service = context.get("learning_service")
        if learning_service:
            learning_service.registrar_instrucao(
                pergunta=text,
                acao="responder_texto",
                resposta=resposta,
                fonte="gpt_assistido"
            )

        return StepResult(True, stop=True)