from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(prefix="/media", tags=["media"])
MEDIA_ROOT = Path(
    r"D:\assistente\mfsim_assistente\backend\data\docs\video"
)

@router.get("/{filename}")
def stream_media(filename: str):
    full_path = MEDIA_ROOT / filename

    if not full_path.exists():
        return {"error": "Arquivo não encontrado"}

    return FileResponse(
        full_path,
        media_type="video/mp4",
        headers={
            "Content-Disposition": "inline",
            "Cache-Control": "no-store",
        }
    )