import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from logic.manager_factory import ManagerFactory
from logic.models.text_request import TextRequest
from backend.config.text_config import TextConfig

def test_text_manager():
    factory = ManagerFactory()
    text_manager = factory.create_text_manager()
    
    print("\n=== Testing Text Manager ===")
    try:
        request = TextRequest(
            text="What is the capital of France?",
            model_id="ibm/granite-20b-multilingual",
            project_id="b7031d21-6edc-492e-8cb5-cd303aa967c7",
            temperature=TextConfig.DEFAULT_PARAMS["temperature"],
            max_tokens=TextConfig.DEFAULT_PARAMS["max_new_tokens"]
        )
        
        result = text_manager.process_text(request)
        print("✓ Successfully processed text:")
        print(f"Request: {request}")
        print(f"Response: {result}")
    except Exception as e:
        print(f"✗ Error: {e}")

test_text_manager() 