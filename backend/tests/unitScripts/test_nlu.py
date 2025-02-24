import sys
import os
# Go up three levels: unitScripts -> tests -> backend -> root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.services.nlu_service import NLUService
from backend.services.credentials_manager import CredentialsManager
from backend.utils.errors import ServiceError, ValidationError

def test_nlu_service():
    """Test NLU service functionality"""
    print("\nTesting NLU Service...")

    # Initialize services
    credentials_manager = CredentialsManager()
    nlu_service = NLUService(credentials_manager)

    # Test 1: Valid analysis
    print("\nTest 1: Valid analysis")
    try:
        text = "IBM's Watson technology helps companies innovate with AI solutions."
        features = {
            "sentiment": {},
            "entities": {},
            "keywords": {}
        }
        result = nlu_service.analyze_text(text, features)
        print("✓ Successfully analyzed text")
        print(f"Result preview: {result.keys()}")
    except Exception as e:
        print(f"✗ Failed to analyze text: {str(e)}")

    # Test 2: Invalid text type
    print("\nTest 2: Invalid text type")
    try:
        result = nlu_service.analyze_text(123, features)
        print("✗ Should have raised validation error")
    except ValidationError as e:
        print(f"✓ Correctly caught validation error: {e.message}")
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")

    # Test 3: Invalid features format
    print("\nTest 3: Invalid features format")
    try:
        result = nlu_service.analyze_text("Some text", "invalid")
        print("✗ Should have raised validation error")
    except ValidationError as e:
        print(f"✓ Correctly caught validation error: {e.message}")
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")

    # Test 4: Empty text
    print("\nTest 4: Empty text")
    try:
        result = nlu_service.analyze_text("", features)
        print("✗ Should have raised validation error")
    except ValidationError as e:
        print(f"✓ Correctly caught validation error: {e.message}")
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")

    # Test 5: Complex analysis
    print("\nTest 5: Complex analysis with all features")
    try:
        text = """IBM's Watson AI technology has revolutionized how businesses 
                 approach artificial intelligence. Companies are excited about 
                 the new possibilities for innovation and growth."""
        features = {
            "sentiment": {},
            "emotion": {},
            "entities": {},
            "keywords": {},
            "categories": {},
            "concepts": {},
            "relations": {},
            "semantic_roles": {}
        }
        result = nlu_service.analyze_text(text, features)
        print("✓ Successfully performed complex analysis")
        print("Found features:")
        for feature, data in result.items():
            print(f"- {feature}: {'✓' if data else '✗'}")
    except Exception as e:
        print(f"✗ Failed complex analysis: {str(e)}")

    print("\nNLU Service testing completed")

if __name__ == "__main__":
    test_nlu_service()