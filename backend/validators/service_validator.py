from typing import Dict, Any, Tuple
from ..utils.errors import ValidationError, AuthenticationError
from ..config.nlu_config import NLUConfig
from ..config.text_config import TextConfig
from ..config.speech_config import SpeechConfig
import os

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

    def validate_tts_request(self, text: str, voice: str, params: dict) -> None:
        """Validate TTS request parameters"""
        if not text or len(text) > SpeechConfig.MAX_TEXT_LENGTH:
            raise ValidationError(
                message="Invalid text length",
                code="INVALID_TEXT",
                details={"max_length": SpeechConfig.MAX_TEXT_LENGTH}
            )
            
        if not voice:
            raise ValidationError(
                message="Voice must be specified",
                code="INVALID_VOICE"
            )
            
        # Validate pitch
        pitch = params.get('pitch', 0)
        if not isinstance(pitch, (int, float)) or not (
            SpeechConfig.PITCH_RANGE[0] <= pitch <= SpeechConfig.PITCH_RANGE[1]
        ):
            raise ValidationError(
                message="Invalid pitch value",
                code="INVALID_PITCH",
                details={"range": SpeechConfig.PITCH_RANGE}
            )
            
        # Validate speed
        speed = params.get('speed', 0)
        if not isinstance(speed, (int, float)) or not (
            SpeechConfig.SPEED_RANGE[0] <= speed <= SpeechConfig.SPEED_RANGE[1]
        ):
            raise ValidationError(
                message="Invalid speed value",
                code="INVALID_SPEED",
                details={"range": SpeechConfig.SPEED_RANGE}
            )

    def validate_audio_file(self, file_path: str) -> None:
        """Validate audio file for STT"""
        if not file_path:
            raise ValidationError(
                message="Audio file path is required",
                code="NO_AUDIO_PATH"
            )

        if not os.path.exists(file_path):
            raise ValidationError(
                message="Audio file not found",
                code="FILE_NOT_FOUND",
                details={"path": file_path}
            )

        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in SpeechConfig.STT_SUPPORTED_FORMATS:
            raise ValidationError(
                message="Unsupported audio format",
                code="UNSUPPORTED_FORMAT",
                details={
                    "format": file_extension,
                    "supported_formats": SpeechConfig.STT_SUPPORTED_FORMATS
                }
            )

        file_size = os.path.getsize(file_path)
        if file_size > SpeechConfig.MAX_AUDIO_SIZE:
            raise ValidationError(
                message=f"Audio file exceeds maximum size of {SpeechConfig.MAX_AUDIO_SIZE/1024/1024}MB",
                code="FILE_TOO_LARGE",
                details={"size": file_size}
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

    @staticmethod
    def validate_text_params(params: Dict[str, Any]) -> None:
        """Validate text generation parameters."""
        required_params = TextConfig.DEFAULT_PARAMS.keys()
        missing = [param for param in required_params if param not in params]
        invalid = [param for param in params if param not in required_params]
        
        if missing or invalid:
            raise ValidationError(
                message="Invalid text generation parameters",
                code="INVALID_TEXT_PARAMS",
                details={
                    "missing_params": missing,
                    "invalid_params": invalid
                }
            )

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

    @staticmethod
    def validate_nlu_request(text: str, features: Dict[str, Any]) -> None:
        """Example combined NLU request validation."""
        if not isinstance(text, str) or not text.strip():
            raise ValidationError(
                message="Text must be a non-empty string",
                code="INVALID_TEXT"
            )
        if not isinstance(features, dict):
            raise ValidationError(
                message="Features must be a dictionary",
                code="INVALID_FEATURES"
            )
        # Then validate the set of features
        ServiceValidator.validate_nlu_features(features)

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