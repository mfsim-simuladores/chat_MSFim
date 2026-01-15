from fastapi import APIRouter, Request

router = APIRouter(prefix="/learning", tags=["learning"])

@router.get("/pending")
def listar(request: Request):
    return request.app.state.learning_repo.list_pending()

@router.post("/approve")
def aprovar(request: Request, question: str, category: str = "Geral"):
    return request.app.state.learning_repo.approve(question, category)
