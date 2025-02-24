import logging
from backend.services.project_service import ProjectService
from logic.utils.file_manager import FileManager

class ProjectManager:
    """Business logic for project operations"""
    
    def __init__(self, project_service: ProjectService, file_manager: FileManager = None):
        self.project_service = project_service
        self.file_manager = file_manager or FileManager()

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
            return {"error": str(e)}

    def get_project_details(self, project_id: str):
        """Get detailed information for a specific project"""
        try:
            projects = self.project_service.list_projects()
            for project in projects:
                if project['metadata']['guid'] == project_id:
                    return {
                        'name': project['entity']['name'],
                        'id': project_id,
                        'description': project['entity'].get('description', ''),
                        'created_at': project['metadata']['created_at']
                    }
            return {"error": "Project not found"}
        except Exception as e:
            return {"error": str(e)}

    def select_project(self, project_id: str):
        """Select a project for use"""
        try:
            return {"status": "Project selected", "project_id": project_id}
        except Exception as e:
            logging.error(f"Error selecting project: {e}")
            return {"status": "Error", "message": str(e)}

    def fetch_and_save_projects(self):
        """Fetch projects and save to file"""
        try:
            projects = self.project_service.list_projects()
            self.file_manager.save_json("user_projects.json", projects)
        except Exception as e:
            logging.error(f"Error saving projects: {e}")

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