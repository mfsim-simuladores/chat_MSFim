class KnowledgeItem:
    def __init__(self, question: str, action: str):
        self.question = question.strip().lower()
        self.action = action.strip()