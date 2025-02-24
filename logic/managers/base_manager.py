import logging
from logic.models.errors import LogicError

class BaseManager:
    """Base class for all managers with common functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def log_error(self, error: LogicError):
        """Log error with details"""
        self.logger.error(
            f"{error.code}: {error.message}",
            extra={"details": error.details}
        ) 