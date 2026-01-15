from sentence_transformers import SentenceTransformer
import numpy as np
import json

class EmbeddingModel:

    def __init__(self, knowledge_path="data/knowledge.json"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.items = []
        self.vetores = None
        self._load_knowledge(knowledge_path)

    def _load_knowledge(self, knowledge_path):
        try:
            with open(knowledge_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            perguntas = []
            itens = []

            for categoria in data:
                for item in categoria.get("Items", []):
                    pergunta = item.get("Question")
                    if pergunta:
                        perguntas.append(pergunta)
                        itens.append(item)

            self.items = itens

            if len(perguntas) > 0:
                self.vetores = self.model.encode(perguntas, convert_to_numpy=True)
            else:
                self.vetores = np.array([])

            print(f"🔍 Embeddings carregados: {len(self.items)} itens.")

        except Exception as e:
            print(f"[EmbeddingModel] Erro ao carregar conhecimento: {e}")
            self.items = []
            self.vetores = np.array([])
