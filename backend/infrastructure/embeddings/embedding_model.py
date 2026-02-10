from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.items = []
        self.vetores = None

    def rebuild(self, knowledge_items):
        """
        Recria embeddings a partir dos itens do KnowledgeManager
        """
        self.items = knowledge_items

        perguntas = [item.question for item in knowledge_items if item.question]

        if perguntas:
            self.vetores = self.model.encode(
                perguntas, convert_to_numpy=True
            )
        else:
            self.vetores = np.array([])

        print(f"🔍 Embeddings recriados: {len(self.items)} itens.")
