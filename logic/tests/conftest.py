import pytest
from unittest.mock import MagicMock
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import managers
from logic.managers.model_manager import ModelManager
from logic.managers.project_manager import ProjectManager
from logic.managers.text_manager import TextManager
from logic.managers.nlu_manager import NLUManager
from logic.managers.tts_manager import TTSManager
from logic.managers.stt_manager import STTManager

# Import validators
from logic.validators.model_validator import ModelValidator
from logic.validators.project_validator import ProjectValidator
from logic.validators.text_validator import TextValidator
from logic.validators.nlu_validator import NLUValidator
from logic.validators.speech_validator import SpeechValidator

# Service mocks
@pytest.fixture
def mock_model_service():
    """Mock model service for manager tests"""
    return MagicMock(name='ModelService')

@pytest.fixture
def mock_project_service():
    """Mock project service for manager tests"""
    return MagicMock(name='ProjectService')

@pytest.fixture
def mock_text_service():
    """Mock text service for manager tests"""
    return MagicMock(name='TextService')

@pytest.fixture
def mock_nlu_service():
    """Mock NLU service for manager tests"""
    return MagicMock(name='NLUService')

@pytest.fixture
def mock_tts_service():
    """Mock TTS service for manager tests"""
    return MagicMock(name='TTSService')

@pytest.fixture
def mock_stt_service():
    """Mock STT service for manager tests"""
    return MagicMock(name='STTService')

# Manager fixtures
@pytest.fixture
def setup_model_manager(mock_model_service):
    """Setup ModelManager instance with mocked dependencies"""
    validator = ModelValidator()
    manager = ModelManager(model_service=mock_model_service, validator=validator)
    return manager

@pytest.fixture
def setup_project_manager(mock_project_service):
    """Setup ProjectManager instance with mocked dependencies"""
    validator = ProjectValidator()
    manager = ProjectManager(project_service=mock_project_service, validator=validator)
    return manager

@pytest.fixture
def setup_text_manager(mock_text_service):
    """Setup TextManager instance with mocked dependencies"""
    validator = TextValidator()
    manager = TextManager(text_service=mock_text_service, validator=validator)
    return manager

@pytest.fixture
def setup_nlu_manager(mock_nlu_service):
    """Setup NLUManager instance with mocked dependencies"""
    validator = NLUValidator()
    manager = NLUManager(nlu_service=mock_nlu_service, validator=validator)
    return manager

@pytest.fixture
def setup_tts_manager(mock_tts_service):
    """Setup TTSManager instance with mocked dependencies"""
    validator = SpeechValidator()
    manager = TTSManager(tts_service=mock_tts_service, validator=validator)
    return manager

@pytest.fixture
def setup_stt_manager(mock_stt_service):
    """Setup STTManager instance with mocked dependencies"""
    validator = SpeechValidator()
    manager = STTManager(stt_service=mock_stt_service, validator=validator)
    return manager

# Other fixtures
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