from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/learning", response_class=HTMLResponse)
def painel_learning(request: Request):
    pendentes = request.app.state.learning_repo.listar_pendentes()

    html = """
    <html>
    <head>
        <title>Aprendizado pendente</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f6f8;
                margin: 40px;
            }
            h2 {
                margin-bottom: 20px;
            }
            .card {
                background: #ffffff;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            .pergunta {
                font-size: 15px;
                font-weight: bold;
                margin-bottom: 15px;
            }
            label {
                font-size: 13px;
                font-weight: bold;
            }
            input, textarea {
                width: 100%;
                padding: 8px;
                margin-top: 5px;
                border-radius: 4px;
                border: 1px solid #ccc;
                font-size: 14px;
            }
            textarea {
                resize: vertical;
            }
            .actions {
                margin-top: 15px;
                display: flex;
                justify-content: flex-end;
            }
            button {
                background: #0078D4;
                color: white;
                border: none;
                padding: 8px 18px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }
            button:hover {
                background: #005fa3;
            }
            .topbar {
                margin-bottom: 30px;
            }
            .count {
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>

    <div class="topbar">
        <h2>Aprendizado pendente</h2>
        <div class="count">{len(pendentes)} itens aguardando validação</div>
    </div>
    """

    for p in pendentes:
        html += f"""
        <div class="card">
            <div class="pergunta">
                {p['instrucao']}
            </div>

            <form action="/learning/approve/{p['id']}" method="post">
                <label>Ação</label>
                <input type="text"
                    name="action"
                    placeholder="ex: responder_texto, start_sim"
                    value="{p.get('acao','')}"
                    required />

                <br/><br/>

                <label>Resposta (opcional)</label>
                <textarea name="response"
                        rows="4"
                        placeholder="Preencha apenas se a ação for responder_texto">{p.get('resposta','')}</textarea>

                <div class="actions">
                    <button type="submit">✔ Aprovar</button>
                </div>
            </form>
        </div>
        """

    html += """
    </body>
    </html>
    """

    return html

