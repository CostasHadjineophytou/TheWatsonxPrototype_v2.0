# Backend Tests

This directory contains tests for the backend components of the Watson Prototype application.

## Test Structure

The tests are organized into the following directories:

- `unit/`: Unit tests for individual backend services and components
- `integration/`: Integration tests for testing interactions between backend components
- `fixtures/`: Common test fixtures and mock data

## Backend vs. Logic Layer Testing

This testing structure focuses on backend components only. The following components should be tested in the backend layer:

- `watson_client.py`: The HTTP client for Watson services
- `iam_token.py`: Token management and authentication
- `service_factory.py`: Service creation and initialization
- `text_service.py`: Text generation functionality
- `service_validator.py`: Parameter validation
- `credentials_manager.py`: Credential management
- `config_validator.py`: Configuration validation
- Other backend services (NLU, TTS, STT, etc.)

**Note**: The file `test_text_manager.py` is currently included but should be moved to logic layer testing in the future, as the TextManager is part of the logic layer, not the backend layer.

## Running Tests

To run the tests, use the following command from the project root:

```bash
pytest backend/tests
```

To run only unit tests:

```bash
pytest backend/tests/unit
```

To run only integration tests:

```bash
pytest backend/tests/integration
```

To run a specific test file:

```bash
pytest backend/tests/unit/test_watson_client.py
```

## Test Coverage

To generate a test coverage report, run:

```bash
pytest --cov=backend backend/tests
```

For a more detailed HTML coverage report:

```bash
pytest --cov=backend --cov-report=html backend/tests
```

This will create a `htmlcov` directory with the coverage report.

## Test Fixtures

Common test fixtures are defined in `conftest.py`. These fixtures provide mock objects and data that can be reused across tests.

Key fixtures include:

- `mock_config`: Mock configuration object
- `mock_credentials`: Mock service credentials
- `mock_iam_token`: Mock IAM token
- `mock_iam_service`: Mock IAM token service
- `mock_watson_client`: Mock Watson client
- `mock_credentials_manager`: Mock credentials manager
- `mock_service_validator`: Mock service validator
- `mock_config_validator`: Mock config validator
- `mock_service_factory`: Mock service factory
- Various response fixtures for testing

## Testing Approach

The testing strategy focuses on the backend layer first, with separate tests for the logic layer to be implemented later. This separation allows for:

1. **Clear Separation of Concerns**: Testing layers independently ensures each layer's responsibilities are properly tested.
2. **Easier Debugging**: When tests fail, it's clearer which layer has the issue.
3. **Reduced Complexity**: Backend tests can focus on API interactions and data processing without the business logic complexity.
4. **Better Test Coverage**: Each layer gets dedicated test coverage.

## Future Logic Layer Testing

When implementing tests for the logic layer, the following components should be tested:

- `text_manager.py`: Business logic for text generation
- `model_manager.py`: Business logic for model management
- `project_manager.py`: Business logic for project management
- Other logic layer managers
- Logic layer validators

## Writing Tests

When writing new tests, follow these guidelines:

1. Place unit tests in the `unit/` directory
2. Place integration tests in the `integration/` directory
3. Use appropriate fixtures from `conftest.py`
4. Follow the naming convention: `test_<component_name>.py` for test files
5. Use descriptive test method names: `test_<method_name>_<scenario>`
6. Include docstrings for test classes and methods
7. Use assertions to verify expected behavior
8. Mock external dependencies to isolate the component being tested

## Test Dependencies

The tests require the following dependencies:

- pytest
- pytest-cov (for coverage reports)
- unittest.mock (for mocking)

These dependencies are included in the `requirements-test.txt` file. 