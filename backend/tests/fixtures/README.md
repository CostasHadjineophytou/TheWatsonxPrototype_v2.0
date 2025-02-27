# Test Fixtures

This directory contains test fixtures used in unit and integration tests for the Watson Prototype backend.

## Purpose

Test fixtures provide reusable test data and mock objects that ensure consistency across tests and reduce duplication in test code. They help make tests more readable, maintainable, and reliable.

## Fixture Structure

The fixtures in this directory are organized as follows:

- **Mock Response Data**: JSON-like structures that mimic API responses from IBM Watson services
- **Sample Input Data**: Example input parameters for testing service methods
- **Helper Functions**: Functions that set up common test scenarios

## Using Fixtures

Fixtures can be imported directly into test files:

```python
from backend.tests.fixtures.sample_responses import MODEL_DETAIL_RESPONSE

def test_model_detail():
    # Use the fixture in your test
    assert MODEL_DETAIL_RESPONSE["model_id"] == "ibm/granite-20b-multilingual"
```

For pytest fixtures, they can be included as parameters in test functions:

```python
def test_service_with_mock_client(mock_watson_client):
    # The mock_watson_client fixture is automatically provided
    service = SomeService(mock_watson_client)
    # Test with the fixture
```

## Available Fixtures

The following fixtures are available:

- **Sample Responses**:
  - `MODELS_RESPONSE`: List of available models
  - `MODEL_DETAIL_RESPONSE`: Details of a specific model
  - `TEXT_GENERATION_RESPONSE`: Response from text generation API
  - `NLU_ANALYSIS_RESPONSE`: Response from NLU analysis API
  - `PROJECTS_RESPONSE`: List of projects
  - `PROJECT_DETAIL_RESPONSE`: Details of a specific project
  - `STT_RESPONSE`: Response from speech-to-text API
  - `TTS_RESPONSE`: Response from text-to-speech API
  - `IAM_TOKEN_RESPONSE`: Response from IAM token service

- **Mock Objects** (in conftest.py):
  - `mock_watson_client`: Mock WatsonClient for testing services
  - `mock_credentials_manager`: Mock CredentialsManager
  - `mock_iam_token`: Mock IAM token
  - `mock_config`: Mock configuration

## Creating New Fixtures

When creating new fixtures, follow these guidelines:

1. **Use descriptive names** that clearly indicate what the fixture represents
2. **Document the fixture** with comments explaining its purpose and structure
3. **Make fixtures reusable** across multiple tests when possible
4. **Organize complex data** in separate modules to keep the code clean
5. **Keep fixtures simple** and focused on specific testing needs 