from domain.knowledge.knowledge_item import KnowledgeItem
from infrastructure.persistence.knowledge_repository import KnowledgeRepository

class KnowledgeManager:
    def __init__(self, repository):
        self.repo = repository
        self._items = None

    def _load(self):
        if self._items is not None:
            return

        raw = self.repo.load_all()
        self._items = []

        for category in raw:
            items = category.get("Items", [])
            for item in items:
                self._items.append(
                    KnowledgeItem(
                        question=item["Question"].strip(),
                        action=item["Action"].strip(),
                        response=item.get("Response")
                    )
                )

    def reload(self):
        self._items = None

    def all_items(self):
        self._load()
        return self._items

    def find_exact(self, question: str):
        self._load()
        q = question.strip().lower()

        for item in self._items:
            if item.question.strip().lower() == q:
                return item
        return None

    def add_item(self, question: str, action: str, response: str | None = None):
        data = self.repo.load_all()

        categoria = next((c for c in data if c["Category"] == "Aprendizado"), None)

        if not categoria:
            categoria = {
                "Category": "Aprendizado",
                "Description": "Conhecimento aprendido incrementalmente",
                "Items": []
            }
            data.append(categoria)

        item = {
            "Question": question.strip(),
            "Action": action.strip()
        }

        if response and response.strip():
            item["Response"] = response.strip()

        categoria["Items"].append(item)
        self.repo.save_all(data)

        self._items = None
