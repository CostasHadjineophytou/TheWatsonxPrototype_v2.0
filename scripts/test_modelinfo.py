import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.model_service import ModelService
from backend.services.watson_client import WatsonClient

def test_model_service():
    watson_client = WatsonClient()
    model_service = ModelService(watson_client)
    granite_info = model_service.get_model_specs("ibm/granite-20b-multilingual")
    print(granite_info)

test_model_service()
