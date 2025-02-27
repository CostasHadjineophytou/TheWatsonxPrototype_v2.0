import pytest
from unittest.mock import patch, MagicMock, call
import os
import pygame

from backend.utils.audio_player import AudioPlayer
from backend.utils.errors import AudioError


class TestAudioPlayer:
    """Tests for the AudioPlayer class"""
    
    @patch('pygame.mixer.init')
    def test_init_success(self, mock_init):
        """Test initializing the AudioPlayer successfully"""
        player = AudioPlayer()
        
        # Check that pygame.mixer.init was called
        mock_init.assert_called_once()
        # Check initial state
        assert player._current_sound is None
        assert player._is_playing is False
        assert player._on_complete_callback is None
    
    @patch('pygame.mixer.init')
    def test_init_error(self, mock_init):
        """Test initializing the AudioPlayer with error"""
        # Mock pygame.mixer.init to raise an exception
        mock_init.side_effect = Exception("Test error")
        
        # Call the constructor and expect exception
        with pytest.raises(AudioError) as exc_info:
            AudioPlayer()
        
        assert exc_info.value.code == "AUDIO_INIT_ERROR"
        mock_init.assert_called_once()
    
    @patch('pygame.mixer.init')
    @patch('os.path.exists')
    @patch('pygame.mixer.Sound')
    def test_play_success(self, mock_sound, mock_exists, mock_init):
        """Test playing audio successfully"""
        # Mock os.path.exists to return True
        mock_exists.return_value = True
        
        # Create a mock Sound object
        mock_sound_instance = MagicMock()
        mock_sound.return_value = mock_sound_instance
        
        # Create the player
        player = AudioPlayer()
        
        # Define a callback function
        callback = MagicMock()
        
        # Call the play method
        audio_path = "test.wav"
        player.play(audio_path, callback)
        
        # Verify the calls
        mock_exists.assert_called_once_with(audio_path)
        mock_sound.assert_called_once_with(audio_path)
        mock_sound_instance.play.assert_called_once()
        
        # Check the state
        assert player._current_sound == mock_sound_instance
        assert player._is_playing is True
        assert player._on_complete_callback == callback
    
    @patch('pygame.mixer.init')
    @patch('os.path.exists')
    def test_play_file_not_found(self, mock_exists, mock_init):
        """Test playing audio with file not found"""
        # Mock os.path.exists to return False
        mock_exists.return_value = False
        
        # Create the player
        player = AudioPlayer()
        
        # Call the play method and expect exception
        audio_path = "nonexistent.wav"
        with pytest.raises(AudioError) as exc_info:
            player.play(audio_path)
        
        assert exc_info.value.code == "FILE_NOT_FOUND"
        mock_exists.assert_called_once_with(audio_path)
    
    @patch('pygame.mixer.init')
    @patch('os.path.exists')
    @patch('pygame.mixer.Sound')
    def test_play_error(self, mock_sound, mock_exists, mock_init):
        """Test playing audio with error"""
        # Mock os.path.exists to return True
        mock_exists.return_value = True
        
        # Mock Sound to raise an exception
        mock_sound.side_effect = Exception("Test error")
        
        # Create the player
        player = AudioPlayer()
        
        # Call the play method and expect exception
        audio_path = "test.wav"
        with pytest.raises(AudioError) as exc_info:
            player.play(audio_path)
        
        assert exc_info.value.code == "PLAYBACK_ERROR"
        mock_exists.assert_called_once_with(audio_path)
        mock_sound.assert_called_once_with(audio_path)
    
    @patch('pygame.mixer.init')
    @patch('os.path.exists')
    @patch('pygame.mixer.Sound')
    def test_play_stop_existing(self, mock_sound, mock_exists, mock_init):
        """Test playing audio when another sound is already playing"""
        # Mock os.path.exists to return True
        mock_exists.return_value = True
        
        # Create mock Sound objects
        mock_sound_instance1 = MagicMock()
        mock_sound_instance2 = MagicMock()
        mock_sound.side_effect = [mock_sound_instance1, mock_sound_instance2]
        
        # Create the player
        player = AudioPlayer()
        
        # Play first sound
        player.play("first.wav")
        
        # Play second sound
        player.play("second.wav")
        
        # Verify that stop was called on the first sound
        mock_sound_instance1.stop.assert_called_once()
        
        # Check the state
        assert player._current_sound == mock_sound_instance2
        assert player._is_playing is True
    
    @patch('pygame.mixer.init')
    @patch('pygame.mixer.Sound')
    def test_stop(self, mock_sound, mock_init):
        """Test stopping audio playback"""
        # Create a mock Sound object
        mock_sound_instance = MagicMock()
        mock_sound.return_value = mock_sound_instance
        
        # Create the player and set up state
        player = AudioPlayer()
        player._current_sound = mock_sound_instance
        player._is_playing = True
        
        # Call the stop method
        player.stop()
        
        # Verify the calls
        mock_sound_instance.stop.assert_called_once()
        
        # Check the state
        assert player._is_playing is False
    
    @patch('pygame.mixer.init')
    def test_stop_no_sound(self, mock_init):
        """Test stopping when no sound is playing"""
        # Create the player
        player = AudioPlayer()
        
        # Call the stop method
        player.stop()
        
        # No assertions needed, just checking that it doesn't raise an exception
    
    @patch('pygame.mixer.init')
    def test_is_playing(self, mock_init):
        """Test checking if audio is playing"""
        # Create the player
        player = AudioPlayer()
        
        # Initial state should be not playing
        assert player.is_playing() is False
        
        # Set playing state
        player._is_playing = True
        assert player.is_playing() is True 