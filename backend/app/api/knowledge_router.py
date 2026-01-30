from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/knowledge")
def process_question(request: Request, q: str):

    pipeline = request.app.state.pipeline
    action = pipeline.interpret(q)

    print("🔍 Usuário perguntou:", q)

    if action is None:
        return {"message": "Não entendi. Aprendendo...", "action": None}

    print("🔎 DEBUG ENVIANDO PARA FLUTTER:", {"action": action})

    return {"mensagem": f"Executando ação '{action}'...", "action": action}
