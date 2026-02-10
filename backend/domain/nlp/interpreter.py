import os
from dotenv import load_dotenv
from domain.nlp.exact_matcher import ExactMatcher
from domain.nlp.fuzzy_matcher import FuzzyMatcher
from domain.nlp.learning_fallback import LearningFallbackStep
from domain.nlp.confirmation_detector import ConfirmationDetector
from domain.nlp.pipeline import InterpreterPipeline
from domain.nlp.semantic_step import SemanticStep
from domain.nlp.wizard_step import WizardStep
from domain.nlp.gpt5_step import GPT5Step


load_dotenv()

def build_interpreter(knowledge_manager, semantic_search, learning_service):

    return InterpreterPipeline(steps=[
        ConfirmationDetector(),
        WizardStep(),
        ExactMatcher(knowledge_manager),
        FuzzyMatcher(knowledge_manager),
        SemanticStep(semantic_search, knowledge_manager),
        GPT5Step(),                    
        LearningFallbackStep(learning_service), 
    ])
