import logging
from backend.services.project_service import ProjectService
from logic.utils.file_manager import FileManager

class ProjectManager:
    """Handles business logic for project operations"""
    
    def __init__(self):
        self.project_service = ProjectService()
        self.file_manager = FileManager()

    def get_projects(self):
        """Get list of projects with simplified information"""
        try:
            projects = self.project_service.list_projects()
            return [
                {
                    "id": project["metadata"]["guid"],
                    "name": project["entity"]["name"]
                }
                for project in projects
            ]
        except Exception as e:
            logging.error(f"Error fetching projects: {e}")
            return []

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