from ibm_watsonx_ai.foundation_models import ModelInference
from backend.services.watson_client import WatsonClient

class TextService:
    """Handles text generation operations"""
    
    def __init__(self, watson_client: WatsonClient):
        self.watson_client = watson_client

    def process_prompt(self, model_id: str, project_id: str, prompt: str, params: dict):
        """Process a prompt using a specific model"""
        try:
            # Creates ModelInference instance for actual text generation
            model = ModelInference(
                model_id=model_id,
                credentials=self.watson_client.credentials,
                project_id=project_id
            )
            return model.generate_text(prompt=prompt, params=params)
        except Exception as e:
            raise RuntimeError(f"Text generation failed: {str(e)}") 