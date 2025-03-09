import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration management"""
    # API Keys and Authentication
    IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
    
    # Service URLs
    IBM_CLOUD_MODELS_URL = os.getenv('IBM_CLOUD_MODELS_URL')
    IBM_CLOUD_PROJECTS_URL = os.getenv('IBM_CLOUD_PROJECTS_URL')
    IAM_TOKEN_URL = os.getenv('IAM_TOKEN_URL')
    IBM_CLOUD_RESOURCE_URL = os.getenv('IBM_CLOUD_RESOURCE_URL')
    IBM_CLOUD_RESOURCE_CONTROLLER_URL = os.getenv('IBM_CLOUD_RESOURCE_CONTROLLER_URL')