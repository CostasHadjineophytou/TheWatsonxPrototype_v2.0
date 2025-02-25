class BackendError(Exception):
    """Base exception for backend layer"""
    def __init__(self, message: str, code: str, details: dict = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(message)

class APIError(BackendError):
    """IBM Cloud API errors"""
    pass

class AuthenticationError(BackendError):
    """Authentication/credential errors"""
    pass

class ServiceError(BackendError):
    """Service-specific errors"""
    pass

class ValidationError(BackendError):
    """Input validation errors"""
    pass

class ConfigurationError(BackendError):
    """Configuration/setup errors"""
    pass

class FileError(BackendError):
    """File operation errors"""
    pass

class AudioError(BackendError):
    """Audio playback related errors"""
    pass 