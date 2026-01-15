from domain.knowledge.knowledge_item import KnowledgeItem

class LearningManager:

    def __init__(self, repository):
        self.repo = repository

    def register(self, question: str, action=None, source="user", response=None):
        self.repo.add_pending({
            "question": question.strip(),
            "action": action,
            "source": source,
            "response": response,
            "status": "pending"
        })

    def list_pending(self):
        return self.repo.load_pending()

    def approve(self, question: str):

        pendings = self.repo.load_pending()
        item = next((p for p in pendings if p["question"].lower() == question.lower()), None)

        if not item:
            return None

        self.repo.remove_pending(question)
        return item
