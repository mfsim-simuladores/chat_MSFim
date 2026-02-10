from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/knowledge",
    tags=["knowledge"]
)

@router.get("/knowledge")
def process_question(request: Request, q: str):

    pipeline = request.app.state.pipeline
    action = pipeline.interpret(q)

    print("🔍 Usuário perguntou:", q)

    if action is None:
        return {"message": "Não entendi. Aprendendo...", "action": None}

    print("🔎 DEBUG ENVIANDO PARA FLUTTER:", {"action": action})

    return {"mensagem": f"Executando ação '{action}'...", "action": action}


@router.post("/reload")
def reload_knowledge(request: Request):

    km = request.app.state.knowledge_manager
    km.reload()

    items = km.all_items()

    embedding = request.app.state.embedding_model
    embedding.rebuild(items)

    return {
        "status": "ok",
        "message": "Knowledge e embeddings recarregados com sucesso"
    }

