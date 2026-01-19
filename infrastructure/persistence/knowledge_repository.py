import json
from typing import List, Dict, Any


class KnowledgeRepository:
    def __init__(self, path: str):
        self.path = path

    def load_all(self) -> List[Dict[str, Any]]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: List[Dict[str, Any]]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
