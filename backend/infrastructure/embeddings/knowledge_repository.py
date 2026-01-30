import json
from typing import List, Dict


class KnowledgeRepository:
    def __init__(self, path: str):
        self.path = path

    def load(self) -> List[Dict]:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return []
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar knowledge: {e}")

    def save_all(self, data: List[Dict]):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
