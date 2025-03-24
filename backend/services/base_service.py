from ..base_component import BaseComponent

class BaseService(BaseComponent):
    """Base class for all backend services
    
    All services inherit from this class, which provides:
    1. Error handling through BaseErrorHandler (via BaseComponent)
    2. Basic validation through BaseValidator (via BaseComponent)
    
    Service-specific classes should override self.validator with their
    specialized validator in their __init__ method if needed.
    """
    
    def __init__(self):
        super().__init__()
