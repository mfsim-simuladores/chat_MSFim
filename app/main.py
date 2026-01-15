from fastapi import FastAPI
from domain.nlp.semantic_search import SemanticSearch
from domain.nlp.interpreter import build_interpreter
from infrastructure.persistence.learning_repository import LearningRepository
from infrastructure.persistence.knowledge_repository import KnowledgeRepository
from infrastructure.embeddings.embedding_model import EmbeddingModel
from domain.knowledge.knowledge_manager import KnowledgeManager
from domain.learning.learning_service import LearningService
from infrastructure.executors.action_executor import ActionExecutor
from app.api.actions_router import router as actions_router
from app.api.knowledge_router import router as knowledge_router
from app.api.learning_router import router as learning_router
from app.api.sse_handler import router as sse_router

def configure_services(app: FastAPI):

    KNOWLEDGE_PATH = "data/knowledge.json"
    PENDING_PATH = "data/pending_learning.json"

    app.state.learning_repo = LearningRepository(PENDING_PATH)
    app.state.learning_service = LearningService(app.state.learning_repo)

    app.state.knowledge_repo = KnowledgeRepository(KNOWLEDGE_PATH)
    app.state.knowledge_manager = KnowledgeManager(app.state.knowledge_repo)

    app.state.embedding_model = EmbeddingModel()
    app.state.semantic_search = SemanticSearch(app.state.embedding_model)


    app.state.pipeline = build_interpreter(
        app.state.knowledge_manager,
        app.state.semantic_search,
        app.state.learning_service
    )

    app.state.executor = ActionExecutor()


    print("🔥 MFSim Assistant carregado com sucesso.")



def create_app() -> FastAPI:
    app = FastAPI(title="MFSim Assistant API")
    configure_services(app)
    app.include_router(actions_router)
    app.include_router(knowledge_router)
    app.include_router(learning_router)
    app.include_router(sse_router)

    return app


app = create_app()
