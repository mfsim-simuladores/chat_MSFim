from datetime import datetime
from domain.knowledge.knowledge_manager import KnowledgeManager
import uuid

class LearningService:

    def __init__(self, repository):
        self.repository = repository

    def _extrair_texto(self, item: dict) -> str:
        return (
            item.get("instrucao")
            or item.get("text")
            or item.get("utterance")
            or ""
        ).strip().lower()

    def registrar_instrucao(self, pergunta, acao=None, fonte="manual", resposta=None):

        pergunta_norm = pergunta.strip().lower()
        existentes = self.repository.listar_todas()

        if any(self._extrair_texto(i) == pergunta_norm for i in existentes):
            return

        nova_instrucao = {
            "id": str(uuid.uuid4()),
            "data": datetime.now().isoformat(),
            "instrucao": pergunta.strip(),
            "acao": acao,
            "resposta": resposta,
            "fonte": fonte,
            "autor": "assistente",
            "status": "pendente",
        }

        self.repository.salvar(nova_instrucao)

    def listar_pendentes(self):
        todas = self.repository.listar_todas()
        return [i for i in todas if i.get("status") == "pendente"]

    def aprovar_instrucao(self, instrucao_id, knowledge_manager, action_override=None):
        itens = self.repository.listar_todas()

        aprovado = None

        for item in itens:
            if item.get("id") == instrucao_id:
                item["status"] = "aprovado"
                if action_override:
                    item["acao"] = action_override
                aprovado = item
                break

        if not aprovado:
            return False

        if not aprovado.get("acao"):
            raise ValueError("Não é possivel aprovar sem ação definida")

        knowledge_manager.add_item(
            question=aprovado["instrucao"],
            action=aprovado.get("acao")
        )

        self.repository.atualizar(
            instrucao_id,
            {"status": "aprovado", "acao": aprovado["acao"]}
        )

        return True