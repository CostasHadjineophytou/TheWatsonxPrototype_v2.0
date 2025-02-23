import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from logic.manager_factory import ManagerFactory
from logic.models.text_request import TextRequest
from backend.config.text_config import TextConfig

class LogicTester:
    def __init__(self):
        self.factory = ManagerFactory()
    
    def test_model_manager(self):
        """Test model manager operations"""
        print("\n=== Testing Model Manager ===")
        try:
            model_manager = self.factory.create_model_manager()
            models = model_manager.get_available_models()
            print(f"✓ Found {len(models)} models")
            for model in models:
                print(f"  - {model}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_project_manager(self):
        """Test project manager operations"""
        print("\n=== Testing Project Manager ===")
        try:
            project_manager = self.factory.create_project_manager()
            projects = project_manager.get_projects()
            print(f"✓ Found {len(projects)} projects")
            for project in projects:
                print(f"  - {project.get('name', 'Unnamed')}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_text_manager(self):
        """Test text manager operations"""
        print("\n=== Testing Text Manager ===")
        try:
            text_manager = self.factory.create_text_manager()
            request = TextRequest(
                text="What is the capital of France?",
                model_id="ibm/granite-20b-multilingual",
                project_id="b7031d21-6edc-492e-8cb5-cd303aa967c7",
                temperature=TextConfig.DEFAULT_PARAMS["temperature"],
                max_tokens=TextConfig.DEFAULT_PARAMS["max_new_tokens"]
            )
            result = text_manager.process_text(request)
            print("✓ Successfully processed text")
            print(f"Response: {result}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_singleton(self):
        """Test that factory is singleton"""
        print("\n=== Testing Factory Singleton ===")
        another_factory = ManagerFactory()
        print(f"Are factories same instance? {self.factory is another_factory}")

    def run_all_tests(self):
        """Run all logic layer tests"""
        print("Starting Logic Layer Tests...")
        self.test_singleton()
        self.test_model_manager()
        self.test_project_manager()
        self.test_text_manager()
        print("\nCompleted Logic Layer Tests")

if __name__ == "__main__":
    tester = LogicTester()
    tester.run_all_tests() 