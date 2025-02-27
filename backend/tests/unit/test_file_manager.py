import pytest
import os
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

from backend.utils.file_manager import FileManager
from backend.utils.errors import FileError


class TestFileManager:
    """Tests for the FileManager class"""
    
    @pytest.fixture
    def file_manager(self):
        """Create a FileManager instance for testing"""
        return FileManager()
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for file operations"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Clean up after tests
        shutil.rmtree(temp_dir)
    
    def test_init(self):
        """Test initializing the FileManager"""
        manager = FileManager()
        assert hasattr(manager, 'logger')
    
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.chmod')
    @patch('pathlib.Path.glob')
    def test_ensure_directories(self, mock_glob, mock_chmod, mock_mkdir):
        """Test ensuring directories exist"""
        # Mock glob to return an empty list (no files)
        mock_glob.return_value = []
        
        # Call the method
        FileManager.ensure_directories()
        
        # Check that mkdir was called for each directory
        assert mock_mkdir.call_count == 4
        # Check that chmod was called for each directory
        assert mock_chmod.call_count == 4
    
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.chmod')
    @patch('pathlib.Path.glob')
    def test_ensure_directories_with_files(self, mock_glob, mock_chmod, mock_mkdir):
        """Test ensuring directories with existing files"""
        # Mock a file in the directory
        mock_file = MagicMock()
        mock_file.is_file.return_value = True
        mock_glob.return_value = [mock_file]
        
        # Call the method
        FileManager.ensure_directories()
        
        # Check that mkdir was called for each directory
        assert mock_mkdir.call_count == 4
        # Check that chmod was called for each directory
        assert mock_chmod.call_count == 4
        # Check that is_file was called
        assert mock_file.is_file.call_count > 0
        # Check that chmod was called on the file
        assert mock_file.chmod.call_count > 0
    
    @patch('pathlib.Path.mkdir')
    def test_save_json_success(self, mock_mkdir, file_manager, temp_dir):
        """Test saving JSON data successfully"""
        # Test data
        test_data = {"key": "value"}
        test_file = os.path.join(temp_dir, "test.json")
        
        # Use a real file for this test
        file_manager.save_json(test_file, test_data)
        
        # Verify the file was created and contains the correct data
        assert os.path.exists(test_file)
        with open(test_file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data == test_data
        
        # Verify mkdir was called
        mock_mkdir.assert_called_once()
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_save_json_error(self, mock_mkdir, mock_file, file_manager):
        """Test saving JSON data with error"""
        # Mock open to raise an exception
        mock_file.side_effect = Exception("Test error")
        
        # Test data
        test_data = {"key": "value"}
        test_file = "test.json"
        
        # Call the method and expect exception
        with pytest.raises(FileError) as exc_info:
            file_manager.save_json(test_file, test_data)
        
        assert exc_info.value.code == "DATA_SAVE_ERROR"
        mock_mkdir.assert_called_once()
    
    def test_load_json_success(self, file_manager, temp_dir):
        """Test loading JSON data successfully"""
        # Create a test JSON file
        test_data = {"key": "value"}
        test_file = os.path.join(temp_dir, "test.json")
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Load the file
        loaded_data = file_manager.load_json(test_file)
        
        # Verify the data was loaded correctly
        assert loaded_data == test_data
    
    def test_load_json_file_not_found(self, file_manager):
        """Test loading JSON with file not found error"""
        # Non-existent file
        test_file = "nonexistent.json"
        
        # Call the method and expect exception
        with pytest.raises(FileError) as exc_info:
            file_manager.load_json(test_file)
        
        assert exc_info.value.code == "FILE_NOT_FOUND"
    
    def test_load_json_invalid_json(self, file_manager, temp_dir):
        """Test loading invalid JSON data"""
        # Create a file with invalid JSON
        test_file = os.path.join(temp_dir, "invalid.json")
        with open(test_file, 'w') as f:
            f.write("{invalid json")
        
        # Call the method and expect exception
        with pytest.raises(FileError) as exc_info:
            file_manager.load_json(test_file)
        
        assert exc_info.value.code == "INVALID_JSON"
    
    @patch('builtins.open', new_callable=mock_open)
    def test_load_json_other_error(self, mock_file, file_manager):
        """Test loading JSON with other error"""
        # Mock open to raise a generic exception
        mock_file.side_effect = Exception("Test error")
        
        # Call the method and expect exception
        with pytest.raises(FileError) as exc_info:
            file_manager.load_json("test.json")
        
        assert exc_info.value.code == "FILE_LOAD_ERROR"
    
    @patch('os.makedirs')
    @patch('os.chmod')
    @patch('time.time')
    @patch('builtins.open', new_callable=mock_open)
    @patch('backend.utils.file_manager.FileManager.cleanup_audio_files')
    def test_save_audio_file_success(self, mock_cleanup, mock_file, mock_time, mock_chmod, mock_makedirs):
        """Test saving audio file successfully"""
        # Mock time to return a fixed timestamp
        mock_time.return_value = 1000.0
        
        # Test data
        audio_content = b"test audio content"
        audio_format = "audio/wav"
        
        # Call the method
        result = FileManager.save_audio_file(audio_content, audio_format)
        
        # Verify the result
        assert result == "data/audio/output_1000000.wav"
        mock_makedirs.assert_called_once()
        mock_file.assert_called_once()
        mock_file().write.assert_called_once_with(audio_content)
        mock_chmod.assert_called_once()
        mock_cleanup.assert_called_once()
    
    @patch('os.makedirs')
    def test_save_audio_file_error(self, mock_makedirs):
        """Test saving audio file with error"""
        # Mock makedirs to raise an exception
        mock_makedirs.side_effect = Exception("Test error")
        
        # Test data
        audio_content = b"test audio content"
        
        # Call the method and expect exception
        with pytest.raises(FileError) as exc_info:
            FileManager.save_audio_file(audio_content)
        
        assert exc_info.value.code == "AUDIO_SAVE_ERROR"
    
    @patch('glob.glob')
    @patch('os.path.getmtime')
    @patch('os.path.exists')
    @patch('os.remove')
    def test_cleanup_audio_files(self, mock_remove, mock_exists, mock_getmtime, mock_glob):
        """Test cleaning up audio files"""
        # Mock glob to return more than max_files
        mock_glob.side_effect = [
            ["file1.wav", "file2.wav"],  # wav files
            ["file3.mp3"],               # mp3 files
            ["file4.ogg", "file5.ogg", "file6.ogg"]  # ogg files
        ]
        # Mock getmtime to return decreasing times (newest first)
        mock_getmtime.side_effect = lambda x: {"file1.wav": 6, "file2.wav": 5, "file3.mp3": 4, 
                                              "file4.ogg": 3, "file5.ogg": 2, "file6.ogg": 1}[x]
        # Mock exists to always return True
        mock_exists.return_value = True
        
        # Call the method with max_files=3
        FileManager.cleanup_audio_files(max_files=3)
        
        # Verify that the oldest 3 files were removed
        assert mock_remove.call_count == 3
        # The files with mtime 3, 2, and 1 should be removed
        mock_remove.assert_any_call("file4.ogg")
        mock_remove.assert_any_call("file5.ogg")
        mock_remove.assert_any_call("file6.ogg")
    
    @patch('glob.glob')
    def test_cleanup_audio_files_no_excess(self, mock_glob):
        """Test cleaning up audio files when there are not too many"""
        # Mock glob to return fewer than max_files
        mock_glob.side_effect = [
            ["file1.wav"],  # wav files
            [],             # mp3 files
            []              # ogg files
        ]
        
        # Call the method
        FileManager.cleanup_audio_files(max_files=5)
        
        # Verify that glob was called but no files were removed
        assert mock_glob.call_count == 3
    
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.chmod')
    @patch('backend.utils.file_manager.FileManager.cleanup_audio_files')
    def test_ensure_audio_directory_success(self, mock_cleanup, mock_chmod, mock_mkdir):
        """Test ensuring audio directory exists"""
        # Call the method
        FileManager.ensure_audio_directory()
        
        # Verify the calls
        mock_mkdir.assert_called_once()
        mock_chmod.assert_called_once()
        mock_cleanup.assert_called_once()
    
    @patch('pathlib.Path.mkdir')
    def test_ensure_audio_directory_error(self, mock_mkdir):
        """Test ensuring audio directory with error"""
        # Mock mkdir to raise an exception
        mock_mkdir.side_effect = Exception("Test error")
        
        # Call the method and expect exception
        with pytest.raises(FileError) as exc_info:
            FileManager.ensure_audio_directory()
        
        assert exc_info.value.code == "DIRECTORY_SETUP_ERROR" 