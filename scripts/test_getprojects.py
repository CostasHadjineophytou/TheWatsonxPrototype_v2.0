import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.project_service import ProjectService

def test_get_projects():
    project_service = ProjectService()
    projects = project_service.list_projects()
    
    print("\n=== Project Details ===")
    for project in projects:
        print(f"\nProject Name: {project['entity']['name']}")
        print(f"Project ID: {project['metadata']['guid']}")
        print(f"Created: {project['metadata']['created_at']}")
        print(f"Description: {project['entity']['description']}")
        
    # Create a simple list of project IDs and names
    project_list = [
        {
            'id': project['metadata']['guid'],
            'name': project['entity']['name']
        }
        for project in projects
    ]
    
    print("\n=== Simplified Project List ===")
    for project in project_list:
        print(f"ID: {project['id']} | Name: {project['name']}")

test_get_projects()
