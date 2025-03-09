from typing import Tuple, Optional
from .base_validator import BaseValidator
from ..models.errors import LogicError
from ..models.requests import NLURequest
from backend.config.nlu_config import NLUConfig

class NLUValidator(BaseValidator):
    """Validates NLU operations"""
    
    def validate(self, request: NLURequest) -> Tuple[bool, Optional[LogicError]]:
        """Validate NLU request"""
        # Validate text
        is_valid, error = self.validate_text(request.text)
        if not is_valid:
            return False, error
            
        # Validate features
        is_valid, error = self.validate_features(request.features)
        if not is_valid:
            return False, error
            
        return True, None
    
    def validate_text(self, text: str) -> Tuple[bool, Optional[LogicError]]:
        """
        Validate input text
        Args:
            text: Text to analyze
        Returns:
            Tuple of (is_valid, error_if_any)
        """
        if not text or not text.strip():
            return False, self.create_error(
                message="Text is required",
                code="EMPTY_TEXT",
                details={"text": text}
            )
            
        if len(text) > NLUConfig.MAX_TEXT_LENGTH:
            return False, self.create_error(
                message=f"Text exceeds maximum length of {NLUConfig.MAX_TEXT_LENGTH:,} characters",
                code="TEXT_TOO_LONG",
                details={"length": len(text)}
            )
            
        return True, None
        
    def validate_features(self, features: list) -> Tuple[bool, Optional[LogicError]]:
        """
        Validate requested features
        Args:
            features: List of NLU features to validate
        Returns:
            Tuple of (is_valid, error_if_any)
        """
        if not features:
            return False, self.create_error(
                message="At least one feature must be selected",
                code="NO_FEATURES",
                details={"features": features}
            )
            
        valid_features = NLUConfig.get_feature_ids()
        invalid_features = [f for f in features if f not in valid_features and f != 'all']
        if invalid_features:
            return False, self.create_error(
                message="Invalid features requested",
                code="INVALID_FEATURES",
                details={
                    "invalid_features": invalid_features,
                    "valid_features": valid_features
                }
            )
            
        return True, None 