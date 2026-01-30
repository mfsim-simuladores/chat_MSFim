import numpy as np
from sentence_transformers import util

class SemanticSearch:

    def __init__(self, embedding_manager):
        self.embedding_manager = embedding_manager

    def buscar(self, texto: str):
        emb = self.embedding_manager.model.encode(
            texto, convert_to_numpy=True
        )
        vetores = self.embedding_manager.vetores

        if vetores is None or not hasattr(vetores, "size") or vetores.size == 0:
            return None

        similaridades = util.cos_sim(emb, vetores)[0]

        idx = int(np.argmax(similaridades))
        score = float(similaridades[idx])

        if score < 0.75:
            return None

        return self.embedding_manager.items[idx]

    def find(self, texto: str):
        return self.buscar(texto)
