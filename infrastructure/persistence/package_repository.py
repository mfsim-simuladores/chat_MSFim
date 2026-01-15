import json
from pathlib import Path
from domain.entitie.PackageItem import PackageItem

class PackageRepository:

    def __init__(self, json_path: str):
        self.json_path = Path(json_path)

    def load_all(self) -> list[PackageItem]:
        if not self.json_path.exists():
            return []

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [PackageItem.from_dict(p) for p in data]

    def save_all(self, items: list[PackageItem]):
        serial = [p.to_dict() for p in items]
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(serial, f, indent=2, ensure_ascii=False)