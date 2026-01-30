class KnowledgeItem:
    def __init__(self, question: str, action: str, response: str = None):
        self.question = question.strip().lower()
        self.action = action.strip()
        self.response = response