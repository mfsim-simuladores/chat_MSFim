import os
from dotenv import load_dotenv
import google.generativeai as genai
from domain.logging.sse_events import SSEEvent
from domain.nlp.pipeline import PipelineStep, StepResult
from domain.state.conversation_state import conversation_state

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") 
if API_KEY:
    genai.configure(api_key=API_KEY)
    

class GeminiConnector:
    SYSTEM_PROMPT = """
Você é um assistente especializado em:
- Simuladores de voo
- Aviação geral
- X-plane 11 e 12
- Instrumentos Garmin (G1000, GNS, GFC, BARON...)
- Operação e sistemas de aeronaves

Responda perguntas informativas de forma clara, técnica, curta e objetiva."""

    @staticmethod
    def responder(prompt: str) -> str | None:
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content([
                {"role": "user", "parts": [GeminiConnector.SYSTEM_PROMPT]},
                {"role": "user", "parts": [prompt]}
            ])

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            return None
        except Exception as e:
            print("[GeminiConnector] Erro:", e)
            return None

class GeminiStep(PipelineStep):

    def run(self, text: str, context: dict) -> StepResult:

        if conversation_state.wizard_running():
            return StepResult(False)

        resposta = GeminiConnector.responder(text)
        if not resposta:
            return StepResult(False, "GEMINI_UNAVAILABLE")

        executor = context.get("executor")
        if executor:
            executor.feedback(
                SSEEvent.message(
                    title="Resposta",
                    message=resposta
                )
            )
            
        return StepResult(True, None)
