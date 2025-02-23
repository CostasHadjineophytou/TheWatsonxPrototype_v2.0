import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.service_factory import ServiceFactory
import json

class ServiceTester:
    def __init__(self):
        self.factory = ServiceFactory()
    
    def test_iam_token(self):
        """Test IAM token service"""
        print("\n=== Testing IAM Token Service ===")
        try:
            token = self.factory.iam_service.get_iam_token()
            print("✓ Successfully retrieved IAM token")
            print(f"Token preview: {token[:50]}...")
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
            models = model_service.list_models()
            # Models response structure might be different
            if isinstance(models, dict):
                models_list = models.get('results', [])
            else:
                models_list = models if isinstance(models, list) else []
            
            print(f"✓ Found {len(models_list)} models")
            for model in models_list:
                name = model['name'] if isinstance(model, dict) else str(model)
                print(f"  - {name}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_credentials_manager(self):
        """Test credentials manager"""
        print("\n=== Testing Credentials Manager ===")
        try:
            cred_manager = self.factory.create_credentials_manager()
            # Test for a specific service
            service_name = "Natural Language Understanding"
            creds = cred_manager.get_service_credentials(service_name)
            print(f"✓ Successfully retrieved credentials for {service_name}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def run_all_tests(self):
        """Run all service tests"""
        print("Starting service tests...")
        self.test_iam_token()
        self.test_project_service()
        self.test_model_service()
        self.test_credentials_manager()
        print("\nCompleted service tests")

if __name__ == "__main__":
    tester = ServiceTester()
    tester.run_all_tests() 