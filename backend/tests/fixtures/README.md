# Test Fixtures

This directory contains test fixtures that provide reusable test data and mock objects for testing the Watson Prototype backend. These fixtures ensure consistency across tests and reduce duplication in test code, making tests more readable, maintainable, and reliable.

## Structure

The fixtures in this directory are organized as follows:

- **Sample Response Data (`sample_responses.py`)**: Contains JSON-like structures that mimic API responses from IBM Watson services. These are used to provide consistent test data for unit and integration tests.

- **Sample Files (`sample_files.py`)**: Contains file paths and binary data for testing file operations. This includes paths to test audio files and sample binary data.

- **Test Files**: Actual files used for testing, such as audio files (`test_audio.wav`).

## Currently Used vs. Future Use

Some fixtures are defined for potential future use:

- **Currently Used**: Audio file paths, sample responses, and binary data are actively used in tests.
- **Future Use**: Text file paths are defined in `sample_files.py` but not currently used, as the application doesn't directly save or process text files.

## Usage

### Importing Constants

You can import constants directly from the fixture files:

```python
from backend.tests.fixtures.sample_responses import TEXT_GENERATION_RESPONSE
from backend.tests.fixtures.sample_files import SAMPLE_AUDIO_FILE_PATH

# Use the constants in your tests
assert response == TEXT_GENERATION_RESPONSE
```

### Using Pytest Fixtures

The fixtures are also available as pytest fixtures in `conftest.py`. These fixtures import the constants from the fixture files:

```python
def test_text_generation(sample_text_response):
    # Use the fixture in your test
    assert result == sample_text_response
```

## Available Fixtures

### Sample Responses (`sample_responses.py`)

- **Model Service Responses**:
  - `MODELS_RESPONSE`: List of available models
  - `MODEL_DETAIL_RESPONSE`: Detailed information about a specific model

- **Text Service Responses**:
  - `TEXT_GENERATION_RESPONSE`: Response from text generation

- **NLU Service Responses**:
  - `NLU_ANALYSIS_RESPONSE`: Response from NLU analysis

- **Project Service Responses**:
  - `PROJECTS_RESPONSE`: List of available projects
  - `PROJECT_DETAIL_RESPONSE`: Detailed information about a specific project

- **STT Service Responses**:
  - `STT_RESPONSE`: Response from speech-to-text service

- **TTS Service Responses**:
  - `TTS_RESPONSE`: Response from text-to-speech service

- **IAM Token Responses**:
  - `IAM_TOKEN_RESPONSE`: Response from IAM token service

### Sample Files (`sample_files.py`)

- **File Paths (Currently Used)**:
  - `SAMPLE_AUDIO_FILE_PATH`: Path to a sample audio file
  - `SAMPLE_OUTPUT_AUDIO_PATH`: Path for output audio files

- **File Paths (Future Use)**:
  - `SAMPLE_TEXT_FILE_PATH`: Path to a sample text file (not currently used)
  - `SAMPLE_OUTPUT_TEXT_PATH`: Path for output text files (not currently used)

- **Binary Data**:
  - `SAMPLE_AUDIO_BINARY`: Sample binary audio data

## Creating New Fixtures

When creating new fixtures, follow these guidelines:

1. **Use Descriptive Names**: Name your fixtures clearly to indicate their purpose.
2. **Document Your Fixtures**: Add comments to explain what each fixture represents.
3. **Keep It Reusable**: Design fixtures to be reusable across multiple tests.
4. **Organize by Type**: Add new fixtures to the appropriate file based on their type.
5. **Keep It Simple**: Fixtures should be simple and focused on a specific testing need.
6. **Mark Future Use**: If creating fixtures for future use, clearly mark them as such.

For constants, add them to the appropriate file in this directory. For pytest fixtures that use these constants, add them to `conftest.py`. 