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
            features_dict = self._prepare_features(features)
            
            # Get raw analysis
            result = self.nlu_service.analyze_text(text, features_dict)
            
            # Transform for business use
            return self._transform_response(result)
            
        except Exception as e:
            self.log_error(e)
            raise

    def _prepare_features(self, features: list) -> dict:
        """Convert feature list to API format"""
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
        return {feature: {} for feature in features}

    def _transform_response(self, result: dict) -> dict:
        """Transform API response to business model"""
        if not result:
            return {}
            
        transformed = {}
        
        if 'sentiment' in result:
            transformed['sentiment'] = {
                'label': result['sentiment']['document']['label'],
                'score': result['sentiment']['document']['score']
            }
            
        if 'emotion' in result:
            transformed['emotion'] = result['emotion']['document']['emotion']
            
        if 'entities' in result:
            transformed['entities'] = [{
                'text': entity['text'],
                'type': entity['type'],
                'confidence': entity['confidence']
            } for entity in result['entities']]
            
        # ... similar transformations for other features
            
        return transformed 