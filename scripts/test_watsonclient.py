import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.watson_client import WatsonClient

def test_watson_client():
    watson_client = WatsonClient()
    print(watson_client.credentials)
    foundation_models = watson_client.client.foundation_models.get_model_specs()
    print([foundation_model['model_id'] for foundation_model in foundation_models['resources']])

test_watson_client()
