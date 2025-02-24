import logging
from backend.services.project_service import ProjectService
from logic.models.errors import LogicError
from logic.validators.project_validator import ProjectValidator
from .base_manager import BaseManager

class ProjectManager(BaseManager):
    """Business logic for project operations"""
    
    def __init__(self, project_service: ProjectService, validator: ProjectValidator):
        super().__init__()
        self.project_service = project_service
        self.validator = validator

    def get_projects(self):
        """Get list of projects with formatted information"""
        try:
            projects = self.project_service.list_projects()
            return [
                {
                    'name': project['entity']['name'],
                    'id': project['metadata']['guid'],
                    'description': project['entity'].get('description', '')
                }
                for project in projects
            ]
        except Exception as e:
            self.log_error(LogicError(
                message="Failed to fetch projects",
                code="PROJECT_FETCH_ERROR",
                details={"error": str(e)}
            ))
            return [{"error": f"Failed to fetch projects: {str(e)}"}]

    def get_project_details(self, project_id: str):
        """Get detailed information for a specific project"""
        try:
            is_valid, error = self.validator.validate(project_id)
            if not is_valid:
                raise error

            projects = self.project_service.list_projects()
            for project in projects:
                if project['metadata']['guid'] == project_id:
                    return {
                        'name': project['entity']['name'],
                        'id': project_id,
                        'description': project['entity'].get('description', ''),
                        'created_at': project['metadata']['created_at']
                    }
            
            raise LogicError(
                message=f"Project {project_id} not found",
                code="PROJECT_NOT_FOUND"
            )
        except LogicError as e:
            self.log_error(e)
            return None
        except Exception as e:
            self.log_error(LogicError(
                message="Failed to get project details",
                code="PROJECT_DETAILS_ERROR",
                details={"project_id": project_id, "error": str(e)}
            ))
            return None

    def select_project(self, project_id: str):
        """Select a project for use"""
        try:
            return {"status": "Project selected", "project_id": project_id}
        except Exception as e:
            logging.error(f"Error selecting project: {e}")
            return {"status": "Error", "message": str(e)}

    def format_project_display(self, project: dict) -> str:
        """Format project name for display"""
        return project.get('name', 'Unnamed')

    def get_project_by_name(self, name: str) -> dict:
        """Get project details by name"""
        projects = self.get_projects()
        for project in projects:
            if project.get('name') == name:
                return project
        return None 