import sys
import os
# Go up two levels: unitScripts -> tests -> backend -> root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.service_factory import ServiceFactory
import json
from backend.config.text_config import TextConfig

class ServiceTester:
    def __init__(self):
        self.factory = ServiceFactory()
    
    def test_iam_token(self):
        """Test IAM token service"""
        print("\n=== Testing IAM Token Service ===")
        try:
            token = self.factory.iam_service.get_iam_token()
            print("✓ Successfully retrieved IAM token")
            print(f"Token preview: {token[:10]}...")
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_project_service(self):
        """Test project service"""
        print("\n=== Testing Project Service ===")
        try:
            project_service = self.factory.create_project_service()
            projects = project_service.list_projects()
            print(f"✓ Found {len(projects)} projects")
            for project in projects:
                print(f"  - {project.get('entity', {}).get('name', 'Unnamed')}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_model_service(self):
        """Test model service"""
        print("\n=== Testing Model Service ===")
        try:
            model_service = self.factory.create_model_service()
            
            # Test model listing
            print("\nListing all models:")
            models = model_service.list_models()
            if isinstance(models, dict):
                models_list = models.get('resources', [])  # Updated to match actual response structure
                print(f"✓ Found {len(models_list)} models")
                for model in models_list:
                    print(f"  - {model.get('model_id', 'Unknown ID')}: {model.get('name', 'Unnamed')}")
            
            # Test specific model details
            print("\nGetting specific model details:")
            model_info = model_service.get_model_specs("ibm/granite-20b-multilingual")
            print(f"✓ Got details for Granite model:")
            print(f"  Name: {model_info.get('name', 'N/A')}")
            print(f"  ID: {model_info.get('model_id', 'N/A')}")
            
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_text_service(self):
        """Test text generation service"""
        print("\n=== Testing Text Service ===")
        try:
            text_service = self.factory.create_text_service()
            
            # Use TextConfig for prompt and parameters
            prompt = TextConfig.SYSTEM_PROMPT
            prompt += "\n\nUser: What is the capital of France?"
            params = TextConfig.DEFAULT_PARAMS
            
            response = text_service.process_prompt(
                model_id="ibm/granite-20b-multilingual",
                project_id="b7031d21-6edc-492e-8cb5-cd303aa967c7",
                prompt=prompt,
                params=params
            )
            print("✓ Successfully generated text:")
            print(f"Prompt: {prompt}")
            print(f"Response: {response}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def run_all_tests(self):
        """Run all service tests"""
        print("Starting service tests...")
        self.test_iam_token()
        self.test_project_service()
        self.test_model_service()
        self.test_text_service()
        print("\nCompleted service tests")

if __name__ == "__main__":
    tester = ServiceTester()
    tester.run_all_tests() 