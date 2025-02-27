import sys
import os
# Go up three levels: unitScripts -> tests -> backend -> root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.services.text_service import TextService
from backend.services.watson_client import WatsonClient
from backend.config.text_config import TextConfig

def test_text_service():
    watson_client = WatsonClient()
    text_service = TextService(watson_client)
    text_config = TextConfig()
    prompt = text_config.SYSTEM_PROMPT
    prompt += "\n\nUser: What is the capital of France?"
    print(prompt)
    params = text_config.DEFAULT_PARAMS
    response = text_service.process_prompt(
        "ibm/granite-20b-multilingual", 
        "project-id", 
        prompt, 
        params
    )
    print(f"\nResponse: {response}")

test_text_service()

