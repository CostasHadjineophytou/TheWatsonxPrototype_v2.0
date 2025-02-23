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
        # Create request with all parameters
        request = TextRequest(
            # Required fields
            text="What is the capital of France?",
            model_id="ibm/granite-20b-multilingual",
            project_id="b7031d21-6edc-492e-8cb5-cd303aa967c7",
            
            # Optional fields with defaults from TextConfig
            system_prompt=TextConfig.SYSTEM_PROMPT,
            temperature=TextConfig.DEFAULT_PARAMS["temperature"],
            max_tokens=TextConfig.DEFAULT_PARAMS["max_new_tokens"],
            top_p=TextConfig.DEFAULT_PARAMS["top_p"],
            top_k=TextConfig.DEFAULT_PARAMS["top_k"],
            min_tokens=TextConfig.DEFAULT_PARAMS["min_new_tokens"],
            repetition_penalty=TextConfig.DEFAULT_PARAMS["repetition_penalty"],
            random_seed=TextConfig.DEFAULT_PARAMS["random_seed"],
            stop_sequences=TextConfig.DEFAULT_PARAMS["stop_sequences"]
        )
        
        # Process the request
        result = text_manager.process_text(request)
        
        # Print results
        print("✓ Successfully processed text")
        print(f"\nRequest Parameters:")
        print(f"  Text: {request.text}")
        print(f"  Model: {request.model_id}")
        print(f"  Temperature: {request.temperature}")
        print(f"  Max Tokens: {request.max_tokens}")
        print(f"  Top P: {request.top_p}")
        print(f"  Top K: {request.top_k}")
        print(f"  Min Tokens: {request.min_tokens}")
        print(f"  Repetition Penalty: {request.repetition_penalty}")
        print(f"\nResponse: {result.get('result', 'No result')}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

test_text_manager() 