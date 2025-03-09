import pytest
from unittest.mock import patch, MagicMock

from backend.services.project_service import ProjectService
from backend.utils.errors import ValidationError, ServiceError, APIError


class TestProjectService:
    """Tests for the ProjectService class"""

    def test_init_with_defaults(self, mock_watson_client):
        """Test initializing ProjectService with default values"""
        service = ProjectService(mock_watson_client)
        assert service.watson_client == mock_watson_client
        assert hasattr(service, 'iam_service')
        assert hasattr(service, 'file_manager')
        assert hasattr(service, 'validator')  # From BaseClient

    def test_init_with_custom_iam(self, mock_watson_client, mock_iam_service):
        """Test initializing ProjectService with custom IAM service"""
        service = ProjectService(mock_watson_client, mock_iam_service)
        assert service.watson_client == mock_watson_client
        assert service.iam_service == mock_iam_service

    @patch('backend.utils.file_manager.FileManager.save_json')
    def test_list_projects_success(self, mock_save_json, mock_watson_client, mock_iam_service):
        """Test listing projects successfully"""
        mock_projects = [
            {
                "id": "test-project-1",
                "name": "Test Project 1"
            }
        ]
        mock_response = {"resources": mock_projects}

        # Set up mocks
        mock_iam_service.get_iam_token.return_value = "test-token"
        
        service = ProjectService(mock_watson_client, mock_iam_service)
        
        with patch.object(service, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = service.list_projects()

            assert result == mock_projects
            mock_iam_service.get_iam_token.assert_called_once()
            mock_request.assert_called_once_with(
                'GET',
                f"{service.projects_url}/v2/projects",
                headers={
                    "Authorization": "Bearer test-token",
                    "Content-Type": "application/json"
                }
            )
            mock_save_json.assert_called_once_with("data/cloud/user_projects.json", mock_projects)

    def test_list_projects_validation_error(self, mock_watson_client, mock_iam_service):
        """Test listing projects with resource validation error"""
        service = ProjectService(mock_watson_client, mock_iam_service)
        
        with patch.object(service.validator, 'validate_resource') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid resource access", "INVALID_RESOURCE")
            
            with pytest.raises(ValidationError) as exc_info:
                service.list_projects()
            
            assert exc_info.value.code == "INVALID_RESOURCE"
            mock_iam_service.get_iam_token.assert_not_called()

    def test_list_projects_api_error(self, mock_watson_client, mock_iam_service):
        """Test listing projects with API error"""
        service = ProjectService(mock_watson_client, mock_iam_service)
        mock_iam_service.get_iam_token.return_value = "test-token"

        with patch.object(service, '_make_request') as mock_request:
            mock_request.side_effect = Exception("API Error")
            
            with pytest.raises(APIError) as exc_info:
                service.list_projects()
            
            assert str(exc_info.value) == "API Error"

    def test_get_project_details_success(self, mock_watson_client, mock_iam_service):
        """Test getting project details successfully"""
        project_id = "test-project-1"
        mock_project = {
            "id": project_id,
            "name": "Test Project 1"
        }
        mock_response = {"resources": [mock_project, {"id": "other-project"}]}
        
        # Set up mocks
        mock_iam_service.get_iam_token.return_value = "test-token"
        
        service = ProjectService(mock_watson_client, mock_iam_service)
        
        with patch.object(service, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = service.get_project_details(project_id)
            
            assert result == mock_project
            mock_iam_service.get_iam_token.assert_called_once()
            mock_request.assert_called_once_with(
                'GET',
                f"{service.projects_url}/v2/projects",
                headers={
                    "Authorization": "Bearer test-token",
                    "Content-Type": "application/json"
                }
            )

    def test_get_project_details_not_found(self, mock_watson_client, mock_iam_service):
        """Test getting details for non-existent project"""
        mock_response = {"resources": [{"id": "other-project"}]}
        
        # Set up mocks
        mock_iam_service.get_iam_token.return_value = "test-token"
        
        service = ProjectService(mock_watson_client, mock_iam_service)
        
        with patch.object(service, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            
            with pytest.raises(ServiceError) as exc_info:
                service.get_project_details("non-existent")
            
            assert exc_info.value.code == "PROJECT_NOT_FOUND"

    def test_get_project_details_invalid_id(self, mock_watson_client, mock_iam_service):
        """Test getting project details with invalid project ID"""
        service = ProjectService(mock_watson_client, mock_iam_service)
        
        with patch.object(service.validator, 'validate_project_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid project ID", "INVALID_PROJECT_ID")
            
            with pytest.raises(ValidationError) as exc_info:
                service.get_project_details("")
            
            assert exc_info.value.code == "INVALID_PROJECT_ID"
            mock_iam_service.get_iam_token.assert_not_called()

    def test_get_project_details_api_error(self, mock_watson_client, mock_iam_service):
        """Test getting project details with API error"""
        mock_iam_service.get_iam_token.return_value = "test-token"
        
        service = ProjectService(mock_watson_client, mock_iam_service)
        
        with patch.object(service, '_make_request') as mock_request:
            mock_request.side_effect = Exception("API Error")
            
            with pytest.raises(APIError) as exc_info:
                service.get_project_details("test-project")
            
            assert str(exc_info.value) == "API Error" 