from typing import List, Dict, Any
from ..utils.errors import ConfigurationError
from ..config.config import Config
from ..config.text_config import TextConfig
from ..config.nlu_config import NLUConfig

class ConfigValidator:
    """Validates all configuration settings"""
    
    @staticmethod
    def validate_config() -> None:
        """Validate base configuration"""
        required_vars = [
            'IBM_CLOUD_API_KEY',
            'IBM_CLOUD_MODELS_URL',
            'IBM_CLOUD_PROJECTS_URL',
            'IAM_TOKEN_URL'
        ]
        
        missing = [var for var in required_vars 
                  if not getattr(Config, var)]
        
        if missing:
            raise ConfigurationError(
                message="Missing required configuration",
                code="MISSING_CONFIG",
                details={"missing": missing}
            )

    @staticmethod
    def validate_text_params(params: Dict[str, Any]) -> None:
        """Validate text generation parameters"""
        required_params = TextConfig.DEFAULT_PARAMS.keys()
        missing = [param for param in required_params if param not in params]
        invalid = [param for param in params if param not in required_params]
        
        if missing or invalid:
            raise ConfigurationError(
                message="Invalid text generation parameters",
                code="INVALID_TEXT_PARAMS",
                details={
                    "missing_params": missing,
                    "invalid_params": invalid
                }
            )

    @staticmethod
    def validate_nlu_features(features: Dict[str, Any]) -> None:
        """Validate NLU features configuration"""
        valid_features = NLUConfig.FEATURES.keys()
        invalid = [feat for feat in features if feat not in valid_features]
        
        if invalid:
            raise ConfigurationError(
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
                raise ConfigurationError(
                    message=f"Invalid parameters for feature: {feature}",
                    code="INVALID_FEATURE_PARAMS",
                    details={
                        "feature": feature,
                        "invalid_params": invalid_params,
                        "valid_params": list(default_params.keys())
                    }
                ) 