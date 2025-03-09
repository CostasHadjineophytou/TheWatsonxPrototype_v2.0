from typing import Dict, List
from backend.services.nlu_service import NLUService
from backend.config.nlu_config import NLUConfig
from ..validators.nlu_validator import NLUValidator
from ..models.requests import NLURequest
from ..models.responses import NLUResponse
from .base_manager import BaseManager

class NLUManager(BaseManager):
    """Business logic for NLU operations"""
    
    def __init__(self, nlu_service: NLUService, validator: NLUValidator):
        super().__init__()
        self.nlu_service = nlu_service
        self.validator = validator

    def analyze_text(self, text: str, features: List[str]) -> Dict:
        """Process NLU analysis request (legacy method)"""
        # Create a request object
        request = NLURequest(text=text, features=features)
        # Use the new method
        response = self._analyze_request(request)
        # Convert response back to dict for backward compatibility
        if response.error:
            return {"error": response.error}
            
        result = {}
        if response.sentiment:
            result['sentiment'] = response.sentiment
        if response.emotion:
            result['emotion'] = response.emotion
        if response.entities:
            result['entities'] = response.entities
        if response.keywords:
            result['keywords'] = response.keywords
        if response.categories:
            result['categories'] = response.categories
        if response.concepts:
            result['concepts'] = response.concepts
        if response.relations:
            result['relations'] = response.relations
        if response.semantic_roles:
            result['semantic_roles'] = response.semantic_roles
            
        return result
        
    def analyze_request(self, request: NLURequest) -> NLUResponse:
        """Process NLU analysis request using data classes"""
        try:
            # Validate text
            is_valid, error = self.validator.validate_text(request.text)
            if not is_valid:
                raise self.handle_validation_error(
                    message=error.message,
                    details=error.details
                )

            # Validate features
            is_valid, error = self.validator.validate_features(request.features)
            if not is_valid:
                raise self.handle_validation_error(
                    message=error.message,
                    details=error.details
                )

            # Convert features to API format
            try:
                if 'all' in request.features:
                    features_dict = NLUConfig.get_all_features()
                else:
                    features_dict = {
                        f_id: NLUConfig.get_feature_params(f_id)
                        for f_id in request.features
                    }
            except Exception as e:
                raise self.handle_business_error(
                    message="Failed to process features configuration",
                    code="FEATURE_CONFIG_ERROR",
                    details={"features": request.features, "error": str(e)}
                )
            
            # Get analysis
            try:
                result = self.nlu_service.analyze_text(request.text, features_dict)
            except Exception as e:
                raise self.handle_business_error(
                    message="NLU analysis failed",
                    code="ANALYSIS_ERROR",
                    details={"error": str(e)}
                )
            
            # Transform response
            transformed = self._transform_response(result)
            if "error" in transformed:
                return NLUResponse(
                    text=request.text,
                    features_analyzed=request.features,
                    error=transformed["error"]
                )
                
            return NLUResponse(
                text=request.text,
                features_analyzed=request.features,
                sentiment=transformed.get('sentiment'),
                emotion=transformed.get('emotion'),
                entities=transformed.get('entities'),
                keywords=transformed.get('keywords'),
                categories=transformed.get('categories'),
                concepts=transformed.get('concepts'),
                relations=transformed.get('relations'),
                semantic_roles=transformed.get('semantic_roles')
            )
            
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to complete NLU analysis")
            return NLUResponse(
                text=request.text,
                features_analyzed=request.features,
                error=error.message
            )
    
    # Alias for backward compatibility
    _analyze_request = analyze_request

    def get_available_features(self) -> list:
        """Get list of available features"""
        try:
            return NLUConfig.get_feature_ids()
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get feature list")
            return []

    def _transform_response(self, result: Dict) -> Dict:
        """Transform API response to business format"""
        if not result:
            return {"error": "No analysis results available"}

        try:
            transformed = {}
            
            # Transform each feature's results
            if 'sentiment' in result:
                transformed['sentiment'] = self._transform_sentiment(result['sentiment'])
            if 'emotion' in result:
                transformed['emotion'] = self._transform_emotion(result['emotion'])
            if 'entities' in result:
                transformed['entities'] = self._transform_entities(result['entities'])
            if 'keywords' in result:
                transformed['keywords'] = self._transform_keywords(result['keywords'])
            if 'categories' in result:
                transformed['categories'] = self._transform_categories(result['categories'])
            if 'concepts' in result:
                transformed['concepts'] = self._transform_concepts(result['concepts'])
            if 'relations' in result:
                transformed['relations'] = self._transform_relations(result['relations'])
            if 'semantic_roles' in result:
                transformed['semantic_roles'] = self._transform_semantic_roles(result['semantic_roles'])

            return transformed
            
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to transform NLU response")
            return {"error": error.message}

    def _transform_sentiment(self, sentiment: Dict) -> Dict:
        """Transform sentiment analysis results"""
        try:
            doc_sentiment = sentiment.get('document', {})
            return {
                'label': doc_sentiment.get('label', 'N/A'),
                'score': doc_sentiment.get('score', 0.0)
            }
        except Exception:
            return {'error': 'Error processing sentiment'}

    def _transform_emotion(self, emotion: Dict) -> Dict:
        """Transform emotion analysis results"""
        try:
            doc_emotion = emotion.get('document', {}).get('emotion', {})
            return {score: value for score, value in doc_emotion.items()}
        except Exception:
            return {'error': 'Error processing emotion'}

    def _transform_entities(self, entities: List[Dict]) -> List[Dict]:
        """Transform entities analysis results"""
        if not entities:
            return []
        return [{
            'text': e.get('text', 'N/A'),
            'type': e.get('type', 'N/A'),
            'confidence': e.get('confidence', 0.0),
            'relevance': e.get('relevance', 0.0)
        } for e in entities]

    def _transform_keywords(self, keywords: List[Dict]) -> List[Dict]:
        """Transform keywords analysis results"""
        if not keywords:
            return []
        return [{
            'text': k.get('text', 'N/A'),
            'relevance': k.get('relevance', 0.0),
            'count': k.get('count', 1)
        } for k in keywords]

    def _transform_categories(self, categories: List[Dict]) -> List[Dict]:
        """Transform categories analysis results"""
        if not categories:
            return []
        return [{
            'label': c.get('label', 'N/A'),
            'score': c.get('score', 0.0)
        } for c in categories]

    def _transform_concepts(self, concepts: List[Dict]) -> List[Dict]:
        """Transform concepts analysis results"""
        if not concepts:
            return []
        return [{
            'text': c.get('text', 'N/A'),
            'relevance': c.get('relevance', 0.0),
            'dbpedia_resource': c.get('dbpedia_resource', '')
        } for c in concepts]

    def _transform_relations(self, relations: List[Dict]) -> List[Dict]:
        """Transform relations analysis results"""
        if not relations:
            return []
        return [{
            'type': r.get('type', 'N/A'),
            'sentence': r.get('sentence', ''),
            'arguments': [{
                'text': a.get('text', 'N/A'),
                'type': a.get('type', '')
            } for a in r.get('arguments', [])]
        } for r in relations]

    def _transform_semantic_roles(self, roles: List[Dict]) -> List[Dict]:
        """Transform semantic roles analysis results"""
        if not roles:
            return []
        return [{
            'subject': r.get('subject', {}).get('text', ''),
            'action': r.get('action', {}).get('text', ''),
            'object': r.get('object', {}).get('text', '')
        } for r in roles] 