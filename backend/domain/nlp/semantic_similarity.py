import numpy as np 

class SemanticSimilarity:
    @staticmethod
    def cosine(a: np.ndarray, b: np.ndarray) -> float:
        if a is None or b is None:
            return 0.0

        na = np.linalg.norm(a)
        nb = np.linalg.norm(b)

        if na == 0 or nb == 0:
            return 0.0

        return float(np.dot(a, b) / (na * nb))