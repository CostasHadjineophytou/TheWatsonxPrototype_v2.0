from .errors import (
    BackendError, APIError, AuthenticationError, 
    ServiceError, ValidationError, ConfigurationError
)

def handle_api_error(error: Exception) -> BackendError:
    """Convert API exceptions to our custom exceptions"""
    error_str = str(error).lower()
    
    if "authentication" in error_str:
        return AuthenticationError(
            message=str(error),
            code="AUTH_ERROR"
        )
    if "configuration" in error_str:
        return ConfigurationError(
            message=str(error),
            code="CONFIG_ERROR"
        )
    if "not found" in error_str:
        return APIError(
            message=str(error),
            code="NOT_FOUND"
        )
    if "rate limit" in error_str:
        return ServiceError(
            message=str(error),
            code="RATE_LIMIT"
        )
        
    return APIError(
        message=str(error),
        code="API_ERROR"
    )
