from typing import Dict, Any, Tuple
from ..utils.errors import ValidationError, AuthenticationError

class ServiceValidator:
    """Validates raw service inputs before API calls"""
    
    @staticmethod
    def validate_credentials(credentials: dict) -> None:
        """Validate IBM Cloud credentials"""
        if not credentials:
            raise AuthenticationError(
                message="No credentials provided",
                code="NO_CREDENTIALS"
            )
        
        if not credentials.get('api_key'):
            raise AuthenticationError(
                message="API key is required",
                code="NO_API_KEY"
            )

    @staticmethod
    def validate_model_params(params: Dict[str, Any]) -> None:
        """Validate model generation parameters"""
        required_params = ['decoding_method', 'max_new_tokens']
        for param in required_params:
            if param not in params:
                raise ValidationError(
                    message=f"Missing required parameter: {param}",
                    code="MISSING_PARAM",
                    details={"param": param}
                )

    @staticmethod
    def validate_project_id(project_id: str) -> None:
        """Validate project ID format"""
        if not project_id or not isinstance(project_id, str):
            raise ValidationError(
                message="Invalid project ID format",
                code="INVALID_PROJECT_ID",
                details={"project_id": project_id}
            )

    @staticmethod
    def validate_model_id(model_id: str) -> None:
        """Validate model ID format"""
        if not model_id or not isinstance(model_id, str):
            raise ValidationError(
                message="Invalid model ID format",
                code="INVALID_MODEL_ID",
                details={"model_id": model_id}
            )

    def validate_nlu_request(self, text: str, features: dict) -> None:
        """Validate NLU service request"""
        if not isinstance(text, str):
            raise ValidationError(
                message="Text must be a string",
                code="INVALID_TEXT_TYPE"
            )

        if not isinstance(features, dict):
            raise ValidationError(
                message="Features must be a dictionary",
                code="INVALID_FEATURES_TYPE"
            )

        # Check for required feature parameters
        for feature, params in features.items():
            if not isinstance(params, dict):
                raise ValidationError(
                    message=f"Parameters for feature '{feature}' must be a dictionary",
                    code="INVALID_FEATURE_PARAMS"
                ) 