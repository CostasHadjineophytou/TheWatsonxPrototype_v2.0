import logging
from backend.utils.base_client import BaseClient
from backend.services.iam_token import IAMTokenService
from backend.config.config import Config
from backend.services.watson_client import WatsonClient

class ProjectService(BaseClient):
    """Handles IBM Cloud project-related API calls"""
    
    def __init__(self, watson_client: WatsonClient = None, iam_service: IAMTokenService = None):
        super().__init__()
        self.iam_service = iam_service or IAMTokenService()
        self.projects_url = Config.IBM_CLOUD_PROJECTS_URL

    def list_projects(self):
        """Get list of all projects from IBM Cloud"""
        try:
            token = self.iam_service.get_iam_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            endpoint = f"{self.projects_url}/v2/projects"
            response = self._make_request('GET', endpoint, headers=headers)
            return response.get('resources', [])
            
        except Exception as e:
            logging.error(f"Failed to list projects: {str(e)}")
            raise RuntimeError(f"Failed to list projects: {str(e)}") 