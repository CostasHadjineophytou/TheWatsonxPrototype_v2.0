from ..models.errors import LogicError
from .base_manager import BaseManager
from backend.services.nlu_service import NLUService

class NLUManager(BaseManager):
    """Business logic for NLU operations"""
    
    def __init__(self, nlu_service: NLUService):
        super().__init__()
        self.nlu_service = nlu_service

    def analyze_text(self, text: str, analysis_types: list) -> dict:
        """Process NLU analysis request"""
        try:
            if not text.strip():
                raise LogicError(
                    message="Please enter text to analyze",
                    code="EMPTY_TEXT"
                )

            if not analysis_types:
                raise LogicError(
                    message="Please select at least one analysis type",
                    code="NO_ANALYSIS_TYPE"
                )

            result = self.nlu_service.analyze_text(text, analysis_types)
            return self._format_response(result)
        except Exception as e:
            self.log_error(LogicError(
                message=str(e),
                code="ANALYSIS_ERROR",
                details={"error": str(e)}
            ))
            return {}

    def _format_response(self, result: dict) -> dict:
        """Format the NLU response"""
        if not result:
            return {}
            
        formatted = {}
        
        # Sentiment
        if 'sentiment' in result:
            formatted['sentiment'] = result['sentiment']['document']['label']
            
        # Emotion
        if 'emotion' in result:
            formatted['emotion'] = result['emotion']['document']['emotion']
            
        # Entities
        if 'entities' in result:
            formatted['entities'] = [
                f"{entity['text']} ({entity['type']})" 
                for entity in result['entities']
            ]
            
        # Keywords
        if 'keywords' in result:
            formatted['keywords'] = [
                f"{kw['text']} ({kw['relevance']:.2f})" 
                for kw in result['keywords']
            ]
            
        # Categories
        if 'categories' in result:
            formatted['categories'] = [
                f"{cat['label']} ({cat['score']:.2f})" 
                for cat in result['categories']
            ]
            
        # Concepts
        if 'concepts' in result:
            formatted['concepts'] = [
                f"{concept['text']} ({concept['relevance']:.2f})" 
                for concept in result['concepts']
            ]
            
        # Relations
        if 'relations' in result:
            formatted['relations'] = [
                self._format_relation(rel) for rel in result['relations']
            ]
            
        # Semantic Roles
        if 'semantic_roles' in result:
            formatted['semantic_roles'] = [
                self._format_semantic_role(role) for role in result['semantic_roles']
            ]
            
        return formatted

    def _format_relation(self, relation: dict) -> str:
        args = relation['arguments']
        return f"{args[0]['text']} {relation['type']} {args[1]['text']}"

    def _format_semantic_role(self, role: dict) -> str:
        return f"{role.get('subject', {}).get('text', '')} {role.get('action', {}).get('text', '')} {role.get('object', {}).get('text', '')}" 