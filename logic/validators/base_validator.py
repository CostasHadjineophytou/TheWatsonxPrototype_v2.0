from typing import Tuple, Optional
from logic.models.errors import LogicError

class BaseValidator:
    """Base class for all validators"""
    
    @staticmethod
    def validate(data) -> Tuple[bool, Optional[LogicError]]:
        """Base validation method"""
        raise NotImplementedError() 