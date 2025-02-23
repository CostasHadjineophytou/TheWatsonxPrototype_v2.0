import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from logic.manager_factory import ManagerFactory
from logic.models.text_request import TextRequest
from logic.models.responses import ModelResponse
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
                if isinstance(model, ModelResponse):
                    print(f"  - {model.name} ({model.id})")
                    print(f"    Type: {model.type}")
                    if model.description:
                        print(f"    Description: {model.description}")
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
                print(f"\nProject Details:")
                print(f"  Name: {project.get('name', 'Unnamed')}")
                print(f"  ID: {project.get('id', 'No ID')}")
                print(f"  Description: {project.get('description', 'No description')}")
        except Exception as e:
            print(f"✗ Error: {e}")

    def test_text_manager(self):
        """Test text manager operations"""
        print("\n=== Testing Text Manager ===")
        try:
            text_manager = self.factory.create_text_manager()
            request = TextRequest(
                # Required fields
                text="What is the capital of France?",
                model_id="ibm/granite-20b-multilingual",
                project_id="b7031d21-6edc-492e-8cb5-cd303aa967c7",
                
                # Optional fields with defaults from TextConfig
                system_prompt=TextConfig.SYSTEM_PROMPT,
                temperature=TextConfig.DEFAULT_PARAMS["temperature"],
                max_tokens=TextConfig.DEFAULT_PARAMS["max_new_tokens"],
                min_tokens=TextConfig.DEFAULT_PARAMS["min_new_tokens"],
                top_k=TextConfig.DEFAULT_PARAMS["top_k"],
                top_p=TextConfig.DEFAULT_PARAMS["top_p"],
                repetition_penalty=TextConfig.DEFAULT_PARAMS["repetition_penalty"],
                random_seed=TextConfig.DEFAULT_PARAMS["random_seed"],
                stop_sequences=TextConfig.DEFAULT_PARAMS["stop_sequences"]
            )
            
            result = text_manager.process_text(request)
            print("✓ Successfully processed text")
            print(f"\nRequest Parameters:")
            print(f"  Text: {request.text}")
            print(f"  Model: {request.model_id}")
            print(f"  Temperature: {request.temperature}")
            print(f"  Max/Min Tokens: {request.max_tokens}/{request.min_tokens}")
            print(f"  Top K/P: {request.top_k}/{request.top_p}")
            print(f"\nResponse: {result.get('result', 'No result')}")
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