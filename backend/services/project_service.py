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
            # Validate credentials
            if self.watson_client:
                self.validator.validate_credentials(self.watson_client.credentials)
            
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
            
        except ValidationError as e:
            # Re-raise validation errors
            raise e
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
            if self.watson_client:
                self.validator.validate_credentials(self.watson_client.credentials)
            self.validator.validate_project_id(project_id)
            
            # Get projects from API
            token = self.iam_service.get_iam_token()
            
            if self.watson_client:
                projects = self.watson_client.get_projects(token)
            else:
                # Fallback to direct API call if watson_client not provided
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                endpoint = f"{self.projects_url}/v2/projects"
                response = self._make_request('GET', endpoint, headers=headers)
                projects = response.get('resources', [])
                
            # Search for the project in the results
            for project in projects:
                if project.get('id') == project_id or project.get('metadata', {}).get('guid') == project_id:
                    return project
            
            # If project not found, raise a specific ServiceError
            raise ServiceError(
                message=f"Project {project_id} not found",
                code="PROJECT_NOT_FOUND",
                details={"project_id": project_id}
            )
            
        except ValidationError as e:
            # Re-raise validation errors directly
            raise e
        except ServiceError as e:
            # Re-raise service errors directly
            raise e
        except Exception as e:
            # Handle unexpected API errors
            raise self.handle_error(e, "Failed to get project details") 