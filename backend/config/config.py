import os
from dotenv import load_dotenv

class Config:
    """Configuration class for the application"""
    
    # Load environment variables
    load_dotenv()
    
    # IBM Cloud API Key
    IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
    
    # Service URLs
    IBM_CLOUD_MODELS_URL = os.getenv('IBM_CLOUD_MODELS_URL')
    
    # IAM token URL
    IAM_TOKEN_URL = os.getenv('IAM_TOKEN_URL')
    
    # IBM Cloud Resource URL
    IBM_CLOUD_RESOURCE_URL = os.getenv('IBM_CLOUD_RESOURCE_URL')
    
    # User Watson Studio projects URL
    IBM_CLOUD_PROJECTS_URL = os.getenv('IBM_CLOUD_PROJECTS_URL')
    
    @classmethod
    def reload(cls):
        """Reload configuration from environment variables"""
        load_dotenv(override=True)
        
        # Reload all environment variables
        cls.IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
        cls.IBM_CLOUD_MODELS_URL = os.getenv('IBM_CLOUD_MODELS_URL')
        cls.IAM_TOKEN_URL = os.getenv('IAM_TOKEN_URL')
        cls.IBM_CLOUD_RESOURCE_URL = os.getenv('IBM_CLOUD_RESOURCE_URL')
        cls.IBM_CLOUD_PROJECTS_URL = os.getenv('IBM_CLOUD_PROJECTS_URL')