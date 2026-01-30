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
            <b>{p['instrucao']}</b><br/><br/>

            <form action="/learning/approve/{p['id']}" method="post">
                
                <label><b>Ação</b></label><br/>
                <input type="text"
                       name="action"
                       placeholder="ex: start_sim ou responder_texto"
                       required
                       style="width: 400px;" />
                <br/><br/>

                <label><b>Resposta (opcional)</b></label><br/>
                <textarea name="response"
                          placeholder="Preencha apenas se a ação for responder_texto"
                          rows="4"
                          style="width: 400px;"></textarea>
                <br/><br/>

                <button type="submit">Aprovar</button>
            </form>
        </li>
        <hr/>
        """

    html += "</ul>"
    return html
