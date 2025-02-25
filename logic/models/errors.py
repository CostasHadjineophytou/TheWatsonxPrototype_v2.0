class LogicError(Exception):
    """Base error for all logic layer errors"""
    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code or "LOGIC_ERROR"
        self.details = details or {}
        super().__init__(message)

class ValidationError(LogicError):
    """For input validation failures"""
    pass

class BusinessError(LogicError):
    """For business rule violations"""
    pass

class DataError(LogicError):
    """Raised when data operations fail"""
    pass