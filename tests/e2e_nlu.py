import pytest
import os
from logic.managers.nlu_manager import NLUManager
from logic.validators.nlu_validator import NLUValidator
from backend.services.nlu_service import NLUService
from backend.config.nlu_config import NLUConfig
from backend.services.credentials_manager import CredentialsManager

class TestNLUEndToEnd:
    """End-to-end tests for NLU functionality"""

    @pytest.fixture
    def setup_nlu_system(self):
        """Setup NLU components with real service"""
        # Create credentials manager
        credentials = CredentialsManager()
        
        # Create real service and components
        service = NLUService(credentials_manager=credentials)
        validator = NLUValidator()
        manager = NLUManager(nlu_service=service, validator=validator)
        return manager

    def test_sentiment_analysis(self, setup_nlu_system):
        """Test sentiment analysis with real service"""
        manager = setup_nlu_system
        
        # Test positive sentiment
        positive_result = manager.analyze_text(
            text="I love this product! It's amazing and works perfectly.",
            features=["sentiment"]
        )
        assert "error" not in positive_result
        assert "sentiment" in positive_result
        assert positive_result["sentiment"]["label"] in ["positive", "neutral", "negative"]
        assert isinstance(positive_result["sentiment"]["score"], float)
        
        # Test negative sentiment
        negative_result = manager.analyze_text(
            text="This is terrible. I'm very disappointed with the service.",
            features=["sentiment"]
        )
        assert "error" not in negative_result
        assert "sentiment" in negative_result
        assert negative_result["sentiment"]["label"] in ["positive", "neutral", "negative"]
        assert isinstance(negative_result["sentiment"]["score"], float)

    def test_entity_extraction(self, setup_nlu_system):
        """Test entity extraction with real service"""
        manager = setup_nlu_system
        
        result = manager.analyze_text(
            text="IBM's CEO Arvind Krishna announced new AI developments in New York last week.",
            features=["entities"]
        )
        
        assert "error" not in result
        assert "entities" in result
        entities = result["entities"]
        
        # Verify entity structure
        for entity in entities:
            assert "text" in entity
            assert "type" in entity
            assert isinstance(entity["confidence"], float)
            assert isinstance(entity["relevance"], float)
        
        # Should find at least some of these entities
        entity_texts = [e["text"].lower() for e in entities]
        assert any(name in entity_texts for name in ["ibm", "arvind krishna", "new york"])

    def test_keyword_extraction(self, setup_nlu_system):
        """Test keyword extraction with real service"""
        manager = setup_nlu_system
        
        result = manager.analyze_text(
            text="Artificial intelligence and machine learning are transforming the technology landscape. Cloud computing and data analytics play crucial roles in modern business.",
            features=["keywords"]
        )
        
        assert "error" not in result
        assert "keywords" in result
        keywords = result["keywords"]
        
        # Verify keyword structure
        for keyword in keywords:
            assert "text" in keyword
            assert isinstance(keyword["relevance"], float)
            assert isinstance(keyword["count"], int)
        
        # Should find some relevant keywords
        keyword_texts = [k["text"].lower() for k in keywords]
        assert any(kw in keyword_texts for kw in ["artificial intelligence", "machine learning", "technology"])

    def test_multiple_features(self, setup_nlu_system):
        """Test analyzing multiple features simultaneously"""
        manager = setup_nlu_system
        
        result = manager.analyze_text(
            text="Google and Microsoft are competing in the cloud computing market. Both companies are investing heavily in artificial intelligence.",
            features=["sentiment", "entities", "keywords"]
        )
        
        assert "error" not in result
        assert all(feature in result for feature in ["sentiment", "entities", "keywords"])
        
        # Verify sentiment
        assert isinstance(result["sentiment"]["score"], (float, int))
        
        # Verify entities
        assert any(e["text"] in ["Google", "Microsoft"] for e in result["entities"])
        
        # Verify keywords
        assert any("cloud" in k["text"].lower() for k in result["keywords"])

    def test_error_handling(self, setup_nlu_system):
        """Test error handling with invalid inputs"""
        manager = setup_nlu_system
        
        # Test with empty text
        empty_result = manager.analyze_text(
            text="",
            features=["sentiment"]
        )
        assert "error" in empty_result
        
        # Test with invalid feature
        invalid_feature_result = manager.analyze_text(
            text="Test text",
            features=["invalid_feature"]
        )
        assert "error" in invalid_feature_result
        
        # Test with text that's too long
        long_text = "test " * (NLUConfig.MAX_TEXT_LENGTH // 4)
        long_result = manager.analyze_text(
            text=long_text,
            features=["sentiment"]
        )
        assert "error" in long_result
