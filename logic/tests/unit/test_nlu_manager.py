import pytest
from unittest.mock import MagicMock

from logic.managers.nlu_manager import NLUManager
from logic.models.errors import ValidationError, LogicError
from logic.validators.nlu_validator import NLUValidator
from backend.config.nlu_config import NLUConfig


class TestNLUManager:
    """Unit tests for NLUManager class"""

    def test_analyze_text_success(self, setup_nlu_manager, mock_nlu_service):
        """Test successful text analysis"""
        # Setup mock response
        mock_response = {
            'sentiment': {
                'document': {
                    'label': 'positive',
                    'score': 0.8
                }
            },
            'emotion': {
                'document': {
                    'emotion': {
                        'joy': 0.7,
                        'sadness': 0.1
                    }
                }
            }
        }
        mock_nlu_service.analyze_text.return_value = mock_response

        # Execute
        manager = setup_nlu_manager
        result = manager.analyze_text(
            text="This is a test text",
            features=['sentiment', 'emotion']
        )

        # Assert
        assert 'sentiment' in result
        assert result['sentiment']['label'] == 'positive'
        assert result['sentiment']['score'] == 0.8
        assert 'emotion' in result
        assert result['emotion']['joy'] == 0.7
        mock_nlu_service.analyze_text.assert_called_once()

    def test_analyze_text_validation_error_empty_text(self, setup_nlu_manager, mock_nlu_service):
        """Test analysis with empty text"""
        # Execute
        manager = setup_nlu_manager
        result = manager.analyze_text(text="", features=['sentiment'])

        # Assert
        assert 'error' in result
        assert 'text is required' in result['error'].lower()
        mock_nlu_service.analyze_text.assert_not_called()

    def test_analyze_text_validation_error_invalid_features(self, setup_nlu_manager, mock_nlu_service):
        """Test analysis with invalid features"""
        # Execute
        manager = setup_nlu_manager
        result = manager.analyze_text(
            text="Test text",
            features=['invalid_feature']
        )

        # Assert
        assert 'error' in result
        assert 'invalid features requested' in result['error'].lower()
        mock_nlu_service.analyze_text.assert_not_called()

    def test_analyze_text_service_error(self, setup_nlu_manager, mock_nlu_service):
        """Test handling of service error"""
        # Setup error
        mock_nlu_service.analyze_text.side_effect = Exception("Service error")

        # Execute
        manager = setup_nlu_manager
        result = manager.analyze_text(
            text="Test text",
            features=['sentiment']
        )

        # Assert
        assert 'error' in result
        assert 'Failed to complete NLU analysis' in result['error']
        mock_nlu_service.analyze_text.assert_called_once()

    def test_get_available_features_success(self, setup_nlu_manager):
        """Test getting available features"""
        # Execute
        manager = setup_nlu_manager
        result = manager.get_available_features()

        # Assert
        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(feature, str) for feature in result)

    def test_transform_sentiment(self, setup_nlu_manager):
        """Test sentiment transformation"""
        # Setup
        sentiment_data = {
            'document': {
                'label': 'positive',
                'score': 0.8
            }
        }

        # Execute
        manager = setup_nlu_manager
        result = manager._transform_sentiment(sentiment_data)

        # Assert
        assert result['label'] == 'positive'
        assert result['score'] == 0.8

    def test_transform_emotion(self, setup_nlu_manager):
        """Test emotion transformation"""
        # Setup
        emotion_data = {
            'document': {
                'emotion': {
                    'joy': 0.7,
                    'sadness': 0.1
                }
            }
        }

        # Execute
        manager = setup_nlu_manager
        result = manager._transform_emotion(emotion_data)

        # Assert
        assert result['joy'] == 0.7
        assert result['sadness'] == 0.1

    def test_transform_entities(self, setup_nlu_manager):
        """Test entities transformation"""
        # Setup
        entities_data = [
            {
                'text': 'IBM',
                'type': 'Company',
                'confidence': 0.9,
                'relevance': 0.8
            }
        ]

        # Execute
        manager = setup_nlu_manager
        result = manager._transform_entities(entities_data)

        # Assert
        assert len(result) == 1
        assert result[0]['text'] == 'IBM'
        assert result[0]['type'] == 'Company'
        assert result[0]['confidence'] == 0.9
        assert result[0]['relevance'] == 0.8 