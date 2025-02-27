import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.config.config import Config
from backend.service_factory import ServiceFactory
from backend.services.iam_token import IAMTokenService
from backend.services.watson_client import WatsonClient
from backend.services.model_service import ModelService
from backend.services.project_service import ProjectService
from backend.services.text_service import TextService
from backend.services.nlu_service import NLUService
from backend.services.tts_service import TTSService
from backend.services.stt_service import STTService
from backend.services.credentials_manager import CredentialsManager
from backend.validators.service_validator import ServiceValidator
from backend.validators.config_validator import ConfigValidator

# Import sample data from fixtures
from backend.tests.fixtures.sample_responses import (
    MODELS_RESPONSE, MODEL_DETAIL_RESPONSE, TEXT_GENERATION_RESPONSE,
    NLU_ANALYSIS_RESPONSE, PROJECTS_RESPONSE, PROJECT_DETAIL_RESPONSE,
    STT_RESPONSE, TTS_RESPONSE, IAM_TOKEN_RESPONSE
)
from backend.tests.fixtures.sample_files import (
    SAMPLE_AUDIO_FILE_PATH, SAMPLE_AUDIO_BINARY
)


@pytest.fixture
def mock_config():
    """Mock configuration with test values"""
    with patch.object(Config, 'IBM_CLOUD_API_KEY', 'test_api_key'), \
         patch.object(Config, 'IBM_CLOUD_MODELS_URL', 'https://test-models-url.com'), \
         patch.object(Config, 'IBM_CLOUD_PROJECTS_URL', 'https://test-projects-url.com'), \
         patch.object(Config, 'IAM_TOKEN_URL', 'https://test-iam-url.com'), \
         patch.object(Config, 'IBM_CLOUD_RESOURCE_URL', 'https://test-resource-url.com'):
        yield Config


@pytest.fixture
def mock_credentials():
    """Mock credentials dictionary"""
    return {
        'api_key': 'test_api_key',
        'url': 'https://test-url.com'
    }


@pytest.fixture
def mock_iam_token():
    """Mock IAM token"""
    return IAM_TOKEN_RESPONSE["access_token"]


@pytest.fixture
def mock_iam_service(mock_iam_token):
    """Mock IAM token service"""
    mock_service = MagicMock(spec=IAMTokenService)
    mock_service.get_token.return_value = mock_iam_token
    return mock_service


@pytest.fixture
def mock_watson_client():
    """Mock Watson client"""
    mock_client = MagicMock(spec=WatsonClient)
    mock_client.credentials = {'api_key': 'test_api_key', 'url': 'https://test-url.com'}
    mock_client.client = MagicMock()
    return mock_client


@pytest.fixture
def mock_credentials_manager():
    """Mock credentials manager"""
    mock_manager = MagicMock(spec=CredentialsManager)
    mock_manager.get_service_credentials.return_value = {
        'apikey': 'test_api_key',
        'url': 'https://test-service-url.com'
    }
    return mock_manager


@pytest.fixture
def mock_service_validator():
    """Mock service validator"""
    return MagicMock(spec=ServiceValidator)


@pytest.fixture
def mock_config_validator():
    """Mock config validator"""
    return MagicMock(spec=ConfigValidator)


@pytest.fixture
def mock_service_factory(mock_watson_client, mock_iam_service):
    """Mock service factory"""
    factory = MagicMock(spec=ServiceFactory)
    factory.watson_client = mock_watson_client
    factory.iam_service = mock_iam_service
    factory.create_model_service.return_value = MagicMock(spec=ModelService)
    factory.create_project_service.return_value = MagicMock(spec=ProjectService)
    factory.create_text_service.return_value = MagicMock(spec=TextService)
    factory.create_nlu_service.return_value = MagicMock(spec=NLUService)
    factory.create_tts_service.return_value = MagicMock(spec=TTSService)
    factory.create_stt_service.return_value = MagicMock(spec=STTService)
    return factory


@pytest.fixture
def sample_model_response():
    """Sample model response data"""
    return MODELS_RESPONSE


@pytest.fixture
def sample_model_detail():
    """Sample model detail response"""
    return MODEL_DETAIL_RESPONSE


@pytest.fixture
def sample_project_response():
    """Sample project response data"""
    return PROJECTS_RESPONSE


@pytest.fixture
def sample_project_detail():
    """Sample project detail response"""
    return PROJECT_DETAIL_RESPONSE


@pytest.fixture
def sample_text_response():
    """Sample text generation response"""
    return TEXT_GENERATION_RESPONSE["generated_text"]


@pytest.fixture
def sample_nlu_response():
    """Sample NLU analysis response"""
    return NLU_ANALYSIS_RESPONSE


@pytest.fixture
def sample_audio_file_path():
    """Sample audio file path"""
    return SAMPLE_AUDIO_FILE_PATH


@pytest.fixture
def sample_tts_response():
    """Sample TTS response (binary audio data)"""
    return SAMPLE_AUDIO_BINARY


@pytest.fixture
def sample_stt_response():
    """Sample STT response"""
    return STT_RESPONSE 