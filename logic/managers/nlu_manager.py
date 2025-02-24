from ..models.errors import LogicError
from .base_manager import BaseManager
from backend.services.nlu_service import NLUService
from ..validators.nlu_validator import NLUValidator

class NLUManager(BaseManager):
    """Business logic for NLU operations"""
    
    def __init__(self, nlu_service: NLUService, validator: NLUValidator):
        super().__init__()
        self.nlu_service = nlu_service
        self.validator = validator

    def analyze_text(self, text: str, features: list) -> dict:
        """Process NLU analysis request"""
        try:
            # Validate inputs
            self.validator.validate_text(text)
            self.validator.validate_features(features)

            # Convert feature list to API format
            try:
                features_dict = self._prepare_features(features)
            except Exception as e:
                raise LogicError(
                    message="Failed to prepare features",
                    code="FEATURE_PREPARATION_ERROR",
                    details={"error": str(e)}
                )
            
            # Get raw analysis
            try:
                result = self.nlu_service.analyze_text(text, features_dict)
            except Exception as e:
                raise LogicError(
                    message="Analysis failed",
                    code="ANALYSIS_ERROR",
                    details={"error": str(e)}
                )
            
            # Transform response
            try:
                return self._transform_response(result)
            except Exception as e:
                raise LogicError(
                    message="Failed to process analysis results",
                    code="TRANSFORM_ERROR",
                    details={"error": str(e)}
                )
            
        except LogicError:
            # Let LogicErrors propagate up
            raise
        except Exception as e:
            # Wrap unexpected errors
            self.log_error(e)
            raise LogicError(
                message="Unexpected error during analysis",
                code="UNEXPECTED_ERROR",
                details={"error": str(e)}
            )

    def _prepare_features(self, features: list) -> dict:
        """Convert feature list to API format"""
        if not features:
            raise LogicError(
                message="No features selected",
                code="NO_FEATURES"
            )

        if 'all' in features:
            return {
                'sentiment': {},
                'emotion': {},
                'entities': {},
                'keywords': {},
                'categories': {},
                'concepts': {},
                'relations': {},
                'semantic_roles': {}
            }

        # Validate against available features
        invalid_features = set(features) - set(self.get_available_features())
        if invalid_features:
            raise LogicError(
                message=f"Invalid features selected: {', '.join(invalid_features)}",
                code="INVALID_FEATURES",
                details={"invalid_features": list(invalid_features)}
            )

        return {feature: {} for feature in features}

    def _transform_response(self, result: dict) -> dict:
        """Transform API response to business model"""
        if not result:
            return {}
            
        transformed = {}
        
        # Transform sentiment
        if 'sentiment' in result:
            transformed['sentiment'] = {
                'label': result['sentiment']['document']['label'],
                'score': result['sentiment']['document']['score']
            }
            
        # Transform emotion
        if 'emotion' in result:
            transformed['emotion'] = result['emotion']['document']['emotion']
            
        # Transform entities
        if 'entities' in result:
            transformed['entities'] = [{
                'text': entity['text'],
                'type': entity['type'],
                'confidence': entity.get('confidence', 0.0),
                'relevance': entity.get('relevance', 0.0)
            } for entity in result['entities']]
            
        # Transform keywords
        if 'keywords' in result:
            transformed['keywords'] = [{
                'text': kw['text'],
                'relevance': kw['relevance'],
                'count': kw.get('count', 1)
            } for kw in result['keywords']]
            
        # Transform categories
        if 'categories' in result:
            transformed['categories'] = [{
                'label': cat['label'],
                'score': cat['score']
            } for cat in result['categories']]
            
        # Transform concepts
        if 'concepts' in result:
            transformed['concepts'] = [{
                'text': concept['text'],
                'relevance': concept['relevance'],
                'dbpedia_resource': concept.get('dbpedia_resource', '')
            } for concept in result['concepts']]
            
        # Transform relations
        if 'relations' in result:
            transformed['relations'] = [{
                'type': rel['type'],
                'sentence': rel['sentence'],
                'arguments': [{
                    'text': arg['text'],
                    'type': arg.get('type', '')
                } for arg in rel['arguments']]
            } for rel in result['relations']]
            
        # Transform semantic roles
        if 'semantic_roles' in result:
            transformed['semantic_roles'] = [{
                'subject': role.get('subject', {}).get('text', ''),
                'action': role.get('action', {}).get('text', ''),
                'object': role.get('object', {}).get('text', '')
            } for role in result['semantic_roles']]
            
        return transformed

    def get_available_features(self) -> list:
        """Get list of available NLU features"""
        return [
            'sentiment',
            'emotion',
            'entities',
            'keywords',
            'categories',
            'concepts',
            'relations',
            'semantic_roles',
            'all'
        ] 