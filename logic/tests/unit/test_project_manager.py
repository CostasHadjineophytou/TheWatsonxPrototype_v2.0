import pytest
from unittest.mock import MagicMock

from logic.managers.project_manager import ProjectManager
from logic.models.errors import ValidationError, LogicError
from logic.validators.project_validator import ProjectValidator
from logic.models.responses import ProjectResponse


class TestProjectManager:
    """Unit tests for ProjectManager class"""

    @pytest.fixture
    def setup_project_manager(self, mock_project_service):
        """Setup ProjectManager instance with mocked dependencies"""
        validator = ProjectValidator()
        manager = ProjectManager(project_service=mock_project_service, validator=validator)
        return manager

    def test_get_projects_success(self, setup_project_manager, mock_project_service):
        """Test successful retrieval of projects"""
        # Setup mock response
        mock_project_service.list_projects.return_value = [
            {
                'metadata': {
                    'guid': 'project1',
                    'created_at': '2024-02-25T12:00:00Z'
                },
                'entity': {
                    'name': 'Project One',
                    'description': 'Description 1'
                }
            },
            {
                'metadata': {
                    'guid': 'project2',
                    'created_at': '2024-02-25T13:00:00Z'
                },
                'entity': {
                    'name': 'Project Two',
                    'description': 'Description 2'
                }
            }
        ]

        # Execute
        manager = setup_project_manager
        result = manager.get_projects()

        # Assert
        assert len(result) == 2
        assert result[0].id == 'project1'
        assert result[0].name == 'Project One'
        assert result[0].description == 'Description 1'
        mock_project_service.list_projects.assert_called_once()

    def test_get_projects_service_error(self, setup_project_manager, mock_project_service):
        """Test handling of service error when getting projects"""
        # Setup error
        mock_project_service.list_projects.side_effect = Exception("Service error")

        # Execute
        manager = setup_project_manager
        result = manager.get_projects()

        # Assert
        assert len(result) == 1
        assert result[0].id == 'ERROR'
        assert result[0].error == 'Failed to fetch projects'
        mock_project_service.list_projects.assert_called_once()

    def test_get_project_details_success(self, setup_project_manager, mock_project_service):
        """Test successful retrieval of project details"""
        # Setup mock response
        mock_project_service.list_projects.return_value = [
            {
                'metadata': {
                    'guid': 'project1',
                    'created_at': '2024-02-25T12:00:00Z'
                },
                'entity': {
                    'name': 'Project One',
                    'description': 'Description 1'
                }
            }
        ]

        # Execute
        manager = setup_project_manager
        result = manager.get_project_details('project1')

        # Assert
        assert result.id == 'project1'
        assert result.name == 'Project One'
        assert result.description == 'Description 1'
        mock_project_service.list_projects.assert_called_once()

    def test_get_project_details_validation_error(self, setup_project_manager, mock_project_service):
        """Test project details with invalid project ID"""
        # Execute
        manager = setup_project_manager
        result = manager.get_project_details('')  # Empty project ID

        # Assert
        assert result.id == 'ERROR'
        assert result.error is not None
        assert 'validation failed' in result.error.lower()
        mock_project_service.list_projects.assert_not_called()

    def test_get_project_details_not_found(self, setup_project_manager, mock_project_service):
        """Test project details with non-existent project ID"""
        # Setup mock response
        mock_project_service.list_projects.return_value = []

        # Execute
        manager = setup_project_manager
        result = manager.get_project_details('nonexistent')

        # Assert
        assert result.id == 'ERROR'
        assert 'not found' in result.error.lower()
        mock_project_service.list_projects.assert_called_once()

    def test_select_project_success(self, setup_project_manager):
        """Test successful project selection"""
        # Execute
        manager = setup_project_manager
        result = manager.select_project('project1')

        # Assert
        assert result['status'] == 'Project selected'
        assert result['project_id'] == 'project1'

    def test_format_project_display(self, setup_project_manager):
        """Test project display formatting"""
        # Setup
        project = ProjectResponse(
            id='project1',
            name='Project One',
            description='Description'
        )

        # Execute
        manager = setup_project_manager
        result = manager.format_project_display(project)

        # Assert
        assert result == 'Project One'

    def test_get_project_by_name_success(self, setup_project_manager, mock_project_service):
        """Test getting project by name"""
        # Setup mock response
        mock_project_service.list_projects.return_value = [
            {
                'metadata': {
                    'guid': 'project1',
                    'created_at': '2024-02-25T12:00:00Z'
                },
                'entity': {
                    'name': 'Project One',
                    'description': 'Description 1'
                }
            }
        ]

        # Execute
        manager = setup_project_manager
        result = manager.get_project_by_name('Project One')

        # Assert
        assert result.id == 'project1'
        assert result.name == 'Project One'
        assert result.description == 'Description 1'
        mock_project_service.list_projects.assert_called_once()

    def test_get_project_by_name_not_found(self, setup_project_manager, mock_project_service):
        """Test getting project by non-existent name"""
        # Setup mock response
        mock_project_service.list_projects.return_value = []

        # Execute
        manager = setup_project_manager
        result = manager.get_project_by_name('Nonexistent Project')

        # Assert
        assert result.id == 'ERROR'
        assert 'not found' in result.error.lower()
        mock_project_service.list_projects.assert_called_once() 