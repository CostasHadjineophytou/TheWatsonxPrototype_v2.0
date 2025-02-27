import logging
from .watson_client import WatsonClient
from .iam_token import IAMTokenService
from backend.config.config import Config
from ..utils.errors import ServiceError, ValidationError
from backend.services.base_client import BaseClient
from ..utils.file_manager import FileManager

class ProjectService(BaseClient):
    """Handles IBM Cloud project-related API calls"""
    
    def __init__(self, watson_client: WatsonClient = None, iam_service: IAMTokenService = None):
        super().__init__()
        self.watson_client = watson_client
        self.iam_service = iam_service or IAMTokenService()
        self.projects_url = Config.IBM_CLOUD_PROJECTS_URL
        self.file_manager = FileManager()

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
            projects = response.get('resources', [])
            
            self.file_manager.save_json("data/cloud/user_projects.json", projects)
            
            return projects
            
        except Exception as e:
            raise self.handle_error(e, "Failed to list projects")

    def get_project_details(self, project_id: str) -> dict:
        """
        Get detailed project information
        
        Args:
            project_id: The ID of the project to retrieve
            
        Returns:
            Dictionary containing project details
            
        Raises:
            ValidationError: If credentials or project ID are invalid
            ServiceError: If the project is not found or API issues occur
        """
        # Validate inputs first
        try:
            self.validator.validate_credentials(self.watson_client.credentials)
            self.validator.validate_project_id(project_id)
        except ValidationError as e:
            # Re-raise validation errors directly
            raise e
            
        # Get projects from API
        try:
            token = self.iam_service.get_token()
            projects = self.watson_client.get_projects(token)
        except Exception as e:
            # Handle unexpected API errors
            raise self.handle_error(e, "Failed to get project details")
        
        # This is not an exception case, but a normal logical flow:
        # Search for the project in the results
        for project in projects:
            if project['metadata']['guid'] == project_id:
                return project
        
        # If project not found, raise a specific ServiceError
        # This is part of the normal logical flow, not exception handling
        raise ServiceError(
            message=f"Project {project_id} not found",
            code="PROJECT_NOT_FOUND",
            details={"project_id": project_id}
        ) 