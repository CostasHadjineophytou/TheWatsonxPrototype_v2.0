from typing import Dict, Any, Tuple
from ..utils.errors import ValidationError
from ..config.nlu_config import NLUConfig
import os

class NLUValidator:
    """Validates raw service inputs before API calls"""

    @staticmethod
    def validate_nlu_features(features: Dict[str, Any]) -> None:
        """Validate NLU features configuration."""
        valid_features = NLUConfig.FEATURES.keys()
        invalid = [feat for feat in features if feat not in valid_features]
        
        if invalid:
            raise ValidationError(
                message="Invalid NLU features",
                code="INVALID_NLU_FEATURES",
                details={
                    "invalid_features": invalid,
                    "valid_features": list(valid_features)
                }
            )

        # Validate feature parameters
        for feature, params in features.items():
            default_params = NLUConfig.get_feature_params(feature)
            invalid_params = [p for p in params if p not in default_params]
            if invalid_params:
                raise ValidationError(
                    message=f"Invalid parameters for feature: {feature}",
                    code="INVALID_FEATURE_PARAMS",
                    details={
                        "feature": feature,
                        "invalid_params": invalid_params,
                        "valid_params": list(default_params.keys())
                    }
                )

    def validate_nlu_request(self, text: str, features: dict) -> None:
        """Validate NLU service request"""
        # Check text type
        if not isinstance(text, str):
            raise ValidationError(
                message="Text must be a string",
                code="INVALID_TEXT_TYPE"
            )

        # Check empty text
        if not text or not text.strip():
            raise ValidationError(
                message="Text cannot be empty",
                code="EMPTY_TEXT"
            )

        # Check features type
        if not isinstance(features, dict):
            raise ValidationError(
                message="Features must be a dictionary",
                code="INVALID_FEATURES_TYPE"
            )

        # Validate feature IDs
        invalid_features = set(features.keys()) - set(NLUConfig.get_feature_ids())
        if invalid_features:
            raise ValidationError(
                message=f"Invalid features: {', '.join(invalid_features)}",
                code="INVALID_FEATURES"
            )
        