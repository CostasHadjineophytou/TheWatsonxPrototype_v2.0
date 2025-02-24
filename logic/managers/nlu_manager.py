from ..models.errors import LogicError
from .base_manager import BaseManager
from backend.services.nlu_service import NLUService
from ..validators.nlu_validator import NLUValidator
from backend.config.nlu_config import NLUConfig

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
            if 'all' in features:
                features_dict = NLUConfig.get_all_features()
            else:
                features_dict = {
                    f_id: NLUConfig.get_feature_params(f_id)
                    for f_id in features
                }
            
            # Get raw analysis
            result = self.nlu_service.analyze_text(text, features_dict)
            
            # Transform for business use
            return self._transform_response(result)
            
        except Exception as e:
            self.log_error(e)
            raise

    def get_available_features(self) -> list:
        """Get list of available features"""
        return NLUConfig.get_feature_ids()

    def _transform_response(self, result: dict) -> dict:
        """Transform API response to business model"""
        if not result:
            return {"error": "No analysis results available"}

        transformed = {}
        
        # Transform sentiment
        if 'sentiment' in result:
            try:
                sentiment = result['sentiment']['document']
                transformed['sentiment'] = {
                    'label': sentiment.get('label', 'N/A'),
                    'score': sentiment.get('score', 0.0)
                }
            except (KeyError, TypeError):
                transformed['sentiment'] = {'error': 'Error processing sentiment'}
            
        # Transform emotion
        if 'emotion' in result:
            try:
                transformed['emotion'] = result['emotion']['document']['emotion']
            except (KeyError, TypeError):
                transformed['emotion'] = {'error': 'Error processing emotions'}
            
        # Transform entities
        if 'entities' in result:
            try:
                entities = result['entities']
                if entities:
                    transformed['entities'] = [{
                        'text': e.get('text', 'N/A'),
                        'type': e.get('type', 'N/A'),
                        'confidence': e.get('confidence', 0.0),
                        'relevance': e.get('relevance', 0.0)
                    } for e in entities]
                else:
                    transformed['entities'] = []
            except (KeyError, TypeError):
                transformed['entities'] = {'error': 'Error processing entities'}

        # Transform keywords
        if 'keywords' in result:
            try:
                keywords = result['keywords']
                if keywords:
                    transformed['keywords'] = [{
                        'text': k.get('text', 'N/A'),
                        'relevance': k.get('relevance', 0.0),
                        'count': k.get('count', 1)
                    } for k in keywords]
                else:
                    transformed['keywords'] = []
            except (KeyError, TypeError):
                transformed['keywords'] = {'error': 'Error processing keywords'}

        # Transform categories
        if 'categories' in result:
            try:
                categories = result['categories']
                if categories:
                    transformed['categories'] = [{
                        'label': c.get('label', 'N/A'),
                        'score': c.get('score', 0.0)
                    } for c in categories]
                else:
                    transformed['categories'] = []
            except (KeyError, TypeError):
                transformed['categories'] = {'error': 'Error processing categories'}

        # Transform concepts
        if 'concepts' in result:
            try:
                concepts = result['concepts']
                if concepts:
                    transformed['concepts'] = [{
                        'text': c.get('text', 'N/A'),
                        'relevance': c.get('relevance', 0.0),
                        'dbpedia_resource': c.get('dbpedia_resource', '')
                    } for c in concepts]
                else:
                    transformed['concepts'] = []
            except (KeyError, TypeError):
                transformed['concepts'] = {'error': 'Error processing concepts'}

        # Transform relations
        if 'relations' in result:
            try:
                relations = result['relations']
                if relations:
                    transformed['relations'] = [{
                        'type': r.get('type', 'N/A'),
                        'sentence': r.get('sentence', ''),
                        'arguments': [{
                            'text': a.get('text', 'N/A'),
                            'type': a.get('type', '')
                        } for a in r.get('arguments', [])]
                    } for r in relations]
                else:
                    transformed['relations'] = []
            except (KeyError, TypeError):
                transformed['relations'] = {'error': 'Error processing relations'}

        # Transform semantic roles
        if 'semantic_roles' in result:
            try:
                roles = result['semantic_roles']
                if roles:
                    transformed['semantic_roles'] = [{
                        'subject': r.get('subject', {}).get('text', ''),
                        'action': r.get('action', {}).get('text', ''),
                        'object': r.get('object', {}).get('text', '')
                    } for r in roles]
                else:
                    transformed['semantic_roles'] = []
            except (KeyError, TypeError):
                transformed['semantic_roles'] = {'error': 'Error processing semantic roles'}

        return transformed 