import pytest
from backend.utils.ssml_builder import SSMLBuilder


class TestSSMLBuilder:
    """Tests for the SSMLBuilder class"""
    
    def test_build_prosody_default_values(self):
        """Test building SSML with default prosody values"""
        text = "Hello, world!"
        result = SSMLBuilder.build_prosody(text)
        
        expected = "<prosody pitch='0%' rate='0%'>Hello, world!</prosody>"
        assert result == expected
    
    def test_build_prosody_custom_pitch(self):
        """Test building SSML with custom pitch"""
        text = "Hello, world!"
        pitch = 50
        result = SSMLBuilder.build_prosody(text, pitch=pitch)
        
        expected = "<prosody pitch='50%' rate='0%'>Hello, world!</prosody>"
        assert result == expected
    
    def test_build_prosody_custom_speed(self):
        """Test building SSML with custom speed"""
        text = "Hello, world!"
        speed = 25
        result = SSMLBuilder.build_prosody(text, speed=speed)
        
        expected = "<prosody pitch='0%' rate='25%'>Hello, world!</prosody>"
        assert result == expected
    
    def test_build_prosody_custom_pitch_and_speed(self):
        """Test building SSML with custom pitch and speed"""
        text = "Hello, world!"
        pitch = 30
        speed = 20
        result = SSMLBuilder.build_prosody(text, pitch=pitch, speed=speed)
        
        expected = "<prosody pitch='30%' rate='20%'>Hello, world!</prosody>"
        assert result == expected
    
    def test_build_prosody_negative_values(self):
        """Test building SSML with negative pitch and speed values"""
        text = "Hello, world!"
        pitch = -25
        speed = -10
        result = SSMLBuilder.build_prosody(text, pitch=pitch, speed=speed)
        
        expected = "<prosody pitch='-25%' rate='-10%'>Hello, world!</prosody>"
        assert result == expected
    
    def test_build_prosody_extreme_values(self):
        """Test building SSML with extreme pitch and speed values"""
        text = "Hello, world!"
        pitch = 100
        speed = -100
        result = SSMLBuilder.build_prosody(text, pitch=pitch, speed=speed)
        
        expected = "<prosody pitch='100%' rate='-100%'>Hello, world!</prosody>"
        assert result == expected
    
    def test_build_prosody_with_special_characters(self):
        """Test building SSML with text containing special characters"""
        text = "Hello & goodbye! <test>"
        result = SSMLBuilder.build_prosody(text)
        
        expected = "<prosody pitch='0%' rate='0%'>Hello & goodbye! <test></prosody>"
        assert result == expected 