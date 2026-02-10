import json
from pathlib import Path
from threading import Lock
from typing import List, Dict, Any


class KnowledgeRepository:
    def __init__(self, path: str):
        self.path = Path(path)
        self._lock = Lock()

    def load_all(self):
        if not self.path.exists():
            return []

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            return data.get("categories", [])

        return data


    def save_all(self, data: List[Dict[str, Any]]) -> None:
        with self._lock:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
