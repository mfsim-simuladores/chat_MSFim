from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/learning", response_class=HTMLResponse)
def painel_learning(request: Request):
    pendentes = request.app.state.learning_repo.listar_pendentes()

    html = "<h2>Aprendizado pendente</h2><ul>"

    for p in pendentes:
        html += f"""
        <li>
            <b>{p['instrucao']}</b><br/>
            <form action="/learning/approve/{p['id']}" method="post">
                <input type="text" name="action"
                        placeholder="ação (ex: responder_modelo)"
                        required />

                <button type="submit">Aprovar</button>
            </form>
        </li><hr/>
        """

    html += "</ul"
    return html