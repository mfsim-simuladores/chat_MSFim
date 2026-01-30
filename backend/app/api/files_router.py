from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/files", tags=["files"])

PDF_DIR = r"D:\assistente\mfsim_assistente\data\pdf"

@router.get("/{filename}")
def get_pdf(filename: str):
    path = os.path.join(PDF_DIR, filename)
    filename = os.path.basename(filename)
    print("Arquivo solicitado:", path)

    if not os.path.exists(path):
        return {"error": "Arquivo não encontrado"}

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=filename
    )
