from .base_validator import BaseValidator
from ..models.errors import ValidationError

class NLUValidator(BaseValidator):
    """Validator for NLU operations"""
    
    def validate_text(self, text: str) -> None:
        """Validate input text"""
        if not text or not text.strip():
            raise ValidationError(
                message="Text cannot be empty",
                code="EMPTY_TEXT"
            )
            
        if len(text) > 50000:  # IBM NLU limit
            raise ValidationError(
                message="Text exceeds maximum length of 50,000 characters",
                code="TEXT_TOO_LONG"
            )

    def validate_features(self, features: list) -> None:
        """Validate selected features"""
        if not features:
            raise ValidationError(
                message="At least one analysis feature must be selected",
                code="NO_FEATURES"
            )
            
        valid_features = {
            'sentiment', 'emotion', 'entities', 'keywords',
            'categories', 'concepts', 'relations', 'semantic_roles', 'all'
        }
        
        invalid_features = set(features) - valid_features
        if invalid_features:
            raise ValidationError(
                message=f"Invalid features selected: {', '.join(invalid_features)}",
                code="INVALID_FEATURES"
            ) 