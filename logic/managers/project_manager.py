import logging
from backend.services.project_service import ProjectService
from ..models.errors import ValidationError
from ..models.responses import ProjectResponse
from ..validators.project_validator import ProjectValidator
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
            raw_projects = self.project_service.list_projects()
            return [
                ProjectResponse(
                    id=project['metadata']['guid'],
                    name=project['entity']['name'],
                    description=project['entity'].get('description', ''),
                    created_at=project['metadata'].get('created_at')
                )
                for project in raw_projects
            ]
        except Exception as e:
            error = self.handle_business_error(
                message="Failed to fetch projects",
                code="PROJECT_FETCH_ERROR",
                details={"error": str(e)}
            )
            return [ProjectResponse(
                id="ERROR",
                name="",
                error=error.message
            )]

    def get_project_details(self, project_id: str) -> ProjectResponse:
        """Get detailed information for a specific project"""
        try:
            is_valid, error = self.validator.validate(project_id)
            if not is_valid:
                raise self.handle_validation_error(
                    message=error.message,
                    details=error.details
                )

            projects = self.project_service.list_projects()
            for project in projects:
                if project['metadata']['guid'] == project_id:
                    return ProjectResponse(
                        id=project_id,
                        name=project['entity']['name'],
                        description=project['entity'].get('description', ''),
                        created_at=project['metadata']['created_at']
                    )
            
            raise self.handle_business_error(
                message=f"Project {project_id} not found",
                code="PROJECT_NOT_FOUND",
                details={"project_id": project_id}
            )
        except ValidationError as e:
            self.log_error(e)
            return ProjectResponse(id="", name="", error=e.message)
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get project details")
            return ProjectResponse(id="", name="", error=error.message)

    def select_project(self, project_id: str) -> dict:
        """Select a project for use"""
        try:
            return {"status": "Project selected", "project_id": project_id}
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to select project")
            return {"status": "Error", "message": error.message}

    def format_project_display(self, project: ProjectResponse) -> str:
        """Format project name for display"""
        if not project:
            return 'Unnamed'
        return project.name

    def get_project_by_name(self, name: str) -> ProjectResponse:
        """Get project details by name"""
        try:
            projects = self.get_projects()
            for project in projects:
                if project.name == name:
                    return project
            
            raise self.handle_business_error(
                message=f"Project with name '{name}' not found",
                code="PROJECT_NAME_NOT_FOUND",
                details={"name": name}
            )
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get project by name")
            return ProjectResponse(id="", name="", error=error.message) 