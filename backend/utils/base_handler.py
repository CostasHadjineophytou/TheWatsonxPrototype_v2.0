from ..validators.service_validator import ServiceValidator
from .error_handling import handle_api_error
import logging

class BaseHandler:
    """Base class for error handling and validation"""
    
    def __init__(self):
        self.validator = ServiceValidator()
    
    def handle_error(self, error: Exception, context: str = None):
        """Standardized error handling"""
        logging.error(f"{context or 'Error'}: {str(error)}")
        if hasattr(error, 'code'):
            return error
        return handle_api_error(error) 