"""
Sample file paths and test files for testing backend services.
These fixtures provide consistent file paths and test data for unit and integration tests.
"""
import os

# Base paths
FIXTURES_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.dirname(FIXTURES_DIR)
BACKEND_DIR = os.path.dirname(TEST_DIR)
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

# Audio file paths - actively used in tests
SAMPLE_AUDIO_FILE_PATH = os.path.join(FIXTURES_DIR, 'test_audio.wav')
SAMPLE_OUTPUT_AUDIO_PATH = os.path.join(FIXTURES_DIR, 'output_audio.wav')

# Text file paths - reserved for future use if needed
# Note: These are defined but not currently used as the application
# doesn't directly save or process text files
SAMPLE_TEXT_FILE_PATH = os.path.join(FIXTURES_DIR, 'test_text.txt')  # Future use
SAMPLE_OUTPUT_TEXT_PATH = os.path.join(FIXTURES_DIR, 'output_text.txt')  # Future use

# Binary data for testing
SAMPLE_AUDIO_BINARY = b'mock audio data for testing' 