import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from logic.manager_factory import ManagerFactory

def test_project_manager():
    factory = ManagerFactory()
    project_manager = factory.create_project_manager()
    
    print("\n=== Testing Project Manager ===")
    try:
        # Get list of projects
        projects = project_manager.get_projects()
        print(f"✓ Found {len(projects)} projects")
        
        # Print project details
        for project in projects:
            print(f"\nProject Details:")
            print(f"  Name: {project.get('name', 'Unnamed')}")
            print(f"  ID: {project.get('id', 'No ID')}")
            print(f"  Description: {project.get('description', 'No description')}")
            
        # Get specific project (using first project's ID if available)
        if projects:
            project_id = projects[0].get('id')
            project_details = project_manager.get_project_details(project_id)
            print(f"\n✓ Got details for project: {project_details.get('name', 'Unnamed')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

test_project_manager() 