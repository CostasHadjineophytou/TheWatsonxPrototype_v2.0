import pytest
from unittest.mock import MagicMock

from logic.managers.model_manager import ModelManager
from logic.models.errors import ValidationError, LogicError
from logic.validators.model_validator import ModelValidator
from logic.models.responses import ModelResponse

class TestModelManager:
    """Unit tests for ModelManager class"""

    @pytest.fixture
    def setup_model_manager(self, mock_model_service):
        """Setup ModelManager instance with mocked dependencies"""
        validator = ModelValidator()
        manager = ModelManager(model_service=mock_model_service, validator=validator)
        return manager

    def test_get_available_models_success(self, setup_model_manager, mock_model_service):
        """Test successful retrieval of available models"""
        # Setup mock response
        mock_model_service.list_models.return_value = {
            'resources': [
                {
                    'model_id': 'model1',
                    'label': 'Model One',
                    'provider': 'Provider A',
                    'short_description': 'Description 1'
                },
                {
                    'model_id': 'model2',
                    'label': 'Model Two',
                    'provider': 'Provider B',
                    'short_description': 'Description 2'
                }
            ]
        }

        # Execute
        manager = setup_model_manager
        result = manager.get_available_models()

        # Assert
        assert len(result) == 2
        assert result[0].id == 'model1'
        assert result[0].name == 'Model One'
        assert result[0].type == 'Provider A'
        assert result[0].description == 'Description 1'
        mock_model_service.list_models.assert_called_once()

    def test_get_available_models_service_error(self, setup_model_manager, mock_model_service):
        """Test handling of service error when getting models"""
        # Setup error
        mock_model_service.list_models.side_effect = Exception("Service error")

        # Execute
        manager = setup_model_manager
        result = manager.get_available_models()

        # Assert
        assert len(result) == 1
        assert result[0].id == 'ERROR'
        assert result[0].error == 'Failed to fetch models'
        mock_model_service.list_models.assert_called_once()

    def test_get_model_details_success(self, setup_model_manager, mock_model_service):
        """Test successful retrieval of model details"""
        # Setup mock response
        mock_model_service.get_model_specs.return_value = {
            'model_id': 'model1',
            'label': 'Model One',
            'provider': 'Provider A',
            'short_description': 'Description 1'
        }

        # Execute
        manager = setup_model_manager
        result = manager.get_model_details('model1')

        # Assert
        assert result.id == 'model1'
        assert result.name == 'Model One'
        assert result.type == 'Provider A'
        assert result.description == 'Description 1'
        mock_model_service.get_model_specs.assert_called_once_with('model1')

    def test_get_model_details_validation_error(self, setup_model_manager, mock_model_service):
        """Test model details with invalid model ID"""
        # Execute
        manager = setup_model_manager
        result = manager.get_model_details('')  # Empty model ID

        # Assert
        assert result.id == 'ERROR'
        assert result.error is not None
        assert 'Model ID is required' in result.error
        mock_model_service.get_model_specs.assert_not_called()

    def test_get_model_details_service_error(self, setup_model_manager, mock_model_service):
        """Test handling of service error when getting model details"""
        # Setup error
        mock_model_service.get_model_specs.side_effect = Exception("Service error")

        # Execute
        manager = setup_model_manager
        result = manager.get_model_details('model1')

        # Assert
        assert result.id == 'ERROR'
        assert 'Failed to get model details' in result.error
        assert 'Service error' in result.error
        mock_model_service.get_model_specs.assert_called_once_with('model1')

    def test_format_model_display(self, setup_model_manager):
        """Test model display formatting"""
        # Setup
        model = ModelResponse(
            id='model1',
            name='Model One',
            type='Provider A',
            description='Description'
        )

        # Execute
        manager = setup_model_manager
        result = manager.format_model_display(model)

        # Assert
        assert result == 'Model One (Provider A)'

    def test_format_model_info(self, setup_model_manager):
        """Test model info formatting"""
        # Setup
        model = ModelResponse(
            id='model1',
            name='Model One',
            type='Provider A',
            description='Description'
        )

        # Execute
        manager = setup_model_manager
        result = manager.format_model_info(model)

        # Assert
        assert 'ID: model1' in result
        assert 'Type: Provider A' in result
        assert 'Description: Description' in result 