class IBMCloudError(Exception):
    """Base exception for IBM Cloud related errors"""
    pass

class AuthenticationError(IBMCloudError):
    """Raised when authentication fails"""
    pass

class ServiceError(IBMCloudError):
    """Raised when a service operation fails"""
    pass

class ConfigurationError(IBMCloudError):
    """Raised when configuration is invalid"""
    pass

def handle_api_error(error: Exception) -> IBMCloudError:
    """Convert API exceptions to our custom exceptions"""
    if "authentication" in str(error).lower():
        return AuthenticationError(str(error))
    if "configuration" in str(error).lower():
        return ConfigurationError(str(error))
    return ServiceError(str(error))
