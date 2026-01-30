import json
import os
import uuid


class LearningRepository:

    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            self._save([])

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def listar_todas(self):
        return self._load()

    def listar_pendentes(self):
        return [r for r in self._load() if r.get("status") == "pendente"]

    def salvar(self, registro):
        data = self._load()
        data.append(registro)
        self._save(data)

    def remover(self, id_):
        data = self._load()
        data = [r for r in data if r.get("id") != id_]
        self._save(data)

    def atualizar(self, id_, novos_dados):
        data = self._load()
        for r in data:
            if r.get("id") == id_:
                r.update(novos_dados)
                break
        self._save(data)

    def registrar_instrucao(self, pergunta: str):
        registro = {
            "id": str(uuid.uuid4()),
            "pergunta": pergunta,
            "status": "pendente"
        }
        self.salvar(registro)
        print(f"[LearningRepository] Pergunta registrada para aprendizado: {pergunta}")
