import json
import os
import numpy as np
from typing import List, Tuple


class EmbeddingRepository:

    def __init__(self, path: str):
        self.path = path

    def load_embeddings(self) -> Tuple[List[str], np.ndarray]:
        if not os.path.exists(self.path):
            return [], np.zeros((0, 384))  
        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        texts = []
        vectors = []

        for entry in raw:
            texts.append(entry["text"])
            vectors.append(np.array(entry["vector"], dtype=float))

        return texts, np.vstack(vectors) if vectors else np.zeros((0, 384))

    def save_embeddings(self, texts: List[str], vectors: np.ndarray):
        data = [
            {"text": txt, "vector": vec.tolist()}
            for txt, vec in zip(texts, vectors)
        ]

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
