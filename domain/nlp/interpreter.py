import os
from dotenv import load_dotenv
import google.generativeai as genai
from domain.nlp.exact_matcher import ExactMatcher
from domain.nlp.fuzzy_matcher import FuzzyMatcher
from domain.nlp.learning_fallback import LearningFallbackStep
from domain.nlp.confirmation_detector import ConfirmationDetector
from domain.nlp.pipeline import InterpreterPipeline
from domain.nlp.semantic_step import SemanticStep
from domain.nlp.gemini_step import GeminiStep
from domain.nlp.wizard_step import WizardStep

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("⚠️ GOOGLE_API_KEY não encontrada. Gemini em modo limitado.")



def build_interpreter(knowledge_manager, semantic_search, learning_service):

    return InterpreterPipeline(steps=[
        ConfirmationDetector(),
        WizardStep(),
        ExactMatcher(knowledge_manager),
        FuzzyMatcher(knowledge_manager),
        SemanticStep(semantic_search, knowledge_manager),
        GeminiStep(),                    
        LearningFallbackStep(learning_service), 
    ])
