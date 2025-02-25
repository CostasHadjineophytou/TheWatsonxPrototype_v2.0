from .base_validator import BaseValidator
from ..models.errors import ValidationError
from backend.config.nlu_config import NLUConfig

class NLUValidator(BaseValidator):
    """Validator for NLU operations"""
    
    def validate_text(self, text: str) -> tuple[bool, ValidationError]:
        """Validate input text"""
        if not text:
            return False, ValidationError(
                message="Text is required",
                code="EMPTY_TEXT",
                details={"text": text}
            )
        return True, None
        
    def validate_features(self, features: list) -> tuple[bool, ValidationError]:
        """Validate requested features"""
        if not features:
            return False, ValidationError(
                message="At least one feature must be selected",
                code="NO_FEATURES",
                details={"features": features}
            )
            
        valid_features = NLUConfig.get_feature_ids()
        invalid_features = [f for f in features if f not in valid_features and f != 'all']
        if invalid_features:
            return False, ValidationError(
                message="Invalid features requested",
                code="INVALID_FEATURES",
                details={"invalid_features": invalid_features}
            )
            
        return True, None 