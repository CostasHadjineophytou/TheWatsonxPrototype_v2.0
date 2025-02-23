import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from logic.manager_factory import ManagerFactory
from logic.models.responses import ModelResponse

def test_model_manager():
    factory = ManagerFactory()
    model_manager = factory.create_model_manager()
    
    print("\n=== Testing Model Manager ===")
    try:
        models = model_manager.get_available_models()
        print(f"✓ Found {len(models)} models")
        for model in models:
            if isinstance(model, ModelResponse):
                print(f"  - {model.name} ({model.id})")
            else:
                print(f"  - {model}")
    except Exception as e:
        print(f"✗ Error: {e}")

test_model_manager() 