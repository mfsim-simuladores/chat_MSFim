from domain.knowledge.knowledge_item import KnowledgeItem

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
                        action=item["Action"].strip()
                    )
                )

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
