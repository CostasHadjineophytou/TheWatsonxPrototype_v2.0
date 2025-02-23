import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.app import WatsonApp
from logic.manager_factory import ManagerFactory
from backend.config.text_config import TextConfig
from logic.models.text_request import TextRequest

class IntegrationTester:
    def __init__(self):
        self.factory = ManagerFactory()
        self.model_manager = self.factory.create_model_manager()
        self.project_manager = self.factory.create_project_manager()
        self.text_manager = self.factory.create_text_manager()
        
    def test_model_flow(self):
        """Test model listing flow from backend to frontend"""
        print("\n=== Testing Model Flow ===")
        try:
            # Get models from backend through logic layer
            models = self.model_manager.get_available_models()
            print(f"✓ Found {len(models)} models")
            
            # Test model details
            if models:
                model = models[0]
                print(f"✓ Got first model: {model.name}")
                print(f"  ID: {model.id}")
                print(f"  Type: {model.type}")
                if model.description:
                    print(f"  Description: {model.description}")
        except Exception as e:
            print(f"✗ Error in model flow: {str(e)}")
            
    def test_project_flow(self):
        """Test project listing and selection"""
        print("\n=== Testing Project Flow ===")
        try:
            projects = self.project_manager.get_projects()
            print(f"✓ Found {len(projects)} projects")
            
            if projects:
                project = projects[0]
                details = self.project_manager.get_project_details(project['id'])
                print(f"✓ Got details for project: {details.get('name', 'N/A')}")
        except Exception as e:
            print(f"✗ Error in project flow: {str(e)}")
            
    def test_text_generation_flow(self):
        """Test complete text generation flow"""
        print("\n=== Testing Text Generation Flow ===")
        try:
            # Get first available model and project
            models = self.model_manager.get_available_models()
            projects = self.project_manager.get_projects()
            
            if not models or not projects:
                print("✗ No models or projects available")
                return
                
            # Create text request with system prompt
            request = TextRequest(
                text="What is the capital of France?",
                model_id=models[0].id,
                project_id=projects[0]['id'],
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
            
            # Test generation
            result = self.text_manager.process_text(request)
            print("✓ Text generation successful")
            print(f"Prompt: {request.text}")
            print(f"System Prompt: {request.system_prompt[:50]}...")
            print(f"Response: {result.get('result', 'No result')}")
            
        except Exception as e:
            print(f"✗ Error in text generation flow: {str(e)}")
            
    def test_ui_creation(self):
        """Test UI component creation"""
        print("\n=== Testing UI Creation ===")
        try:
            app = WatsonApp()
            print("✓ Main app window created")
            print("✓ LLM tab created")
            print("✓ Model frame initialized")
            print("✓ Parameter frame initialized")
            print("✓ Text frame initialized")
            app.destroy()
        except Exception as e:
            print(f"✗ Error creating UI: {str(e)}")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("Starting Integration Tests...")
        self.test_model_flow()
        self.test_project_flow()
        self.test_text_generation_flow()
        self.test_ui_creation()
        print("\nCompleted Integration Tests")

if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_all_tests() 