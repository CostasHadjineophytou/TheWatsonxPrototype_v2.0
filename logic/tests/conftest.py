import pytest
from unittest.mock import MagicMock
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.services.nlu_service import NLUService
from backend.services.tts_service import TTSService
from backend.services.stt_service import STTService
from backend.services.model_service import ModelService
from backend.services.text_service import TextService
from backend.services.project_service import ProjectService

@pytest.fixture
def mock_model_service():
    """Mock model service for manager tests"""
    mock_service = MagicMock(spec=ModelService)
    return mock_service

@pytest.fixture
def mock_project_service():
    """Mock model service for manager tests"""
    mock_service = MagicMock(spec=ProjectService)
    return mock_service

@pytest.fixture
def mock_text_service():
    """Mock model service for manager tests"""
    mock_service = MagicMock(spec=TextService)
    return mock_service

@pytest.fixture
def mock_nlu_service():
    """Mock NLU service for manager tests"""
    mock_service = MagicMock(spec=NLUService)
    return mock_service


@pytest.fixture
def mock_tts_service():
    """Mock TTS service for manager tests"""
    mock_service = MagicMock(spec=TTSService)
    return mock_service


@pytest.fixture
def mock_stt_service():
    """Mock STT service for manager tests"""
    mock_service = MagicMock(spec=STTService)
    return mock_service


@pytest.fixture
def mock_credentials():
    """Mock credentials for manager tests"""
    return {
        'api_key': 'test_api_key',
        'url': 'test_url'
    }


@pytest.fixture
def sample_text_data():
    """Sample text data for text processing tests"""
    return {
        'input': 'Sample input text',
        'expected_output': 'Expected processed text',
        'metadata': {
            'source': 'test',
            'timestamp': '2024-02-26T00:00:00Z'
        }
    } 