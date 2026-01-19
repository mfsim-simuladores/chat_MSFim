from fastapi import APIRouter, Request, Form
from domain.learning.learning_service import LearningService
from domain.knowledge.knowledge_manager import KnowledgeManager

router = APIRouter(prefix="/learning", tags=["learning"])

@router.get("/pending")
def listar(request: Request):
    return request.app.state.learning_repo.list_pending()

@router.post("/approve/{instrucao_id}")
def aprovar(request: Request, instrucao_id: str, action: str = Form(...)):

    learning_service = request.app.state.learning_service
    knowledge_manager = request.app.state.knowledge_manager

    ok = learning_service.aprovar_instrucao(
        instrucao_id=instrucao_id,
        knowledge_manager=knowledge_manager,
        action_override=action
    )

    if not ok:
        return {"status": "erro", "message": "Instrução não encontrada"}

    return{
        "status": "ok",
        "message": "Instrução aprovada e incorporada ao conhecimento"
    }