from fastapi import APIRouter, Request
from app.api.sse_handler import sse_run_action

router = APIRouter(prefix="/actions")

@router.get("/run")
async def run_action(request: Request, text: str):
    return await sse_run_action(request, text)
