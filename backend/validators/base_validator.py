from ..utils.errors import AuthenticationError

class BaseValidator:
    """Base validator with common validation methods used across services"""
    
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
    def validate_resource() -> None:
        """Validate resource access. Placeholder for now."""
        pass
