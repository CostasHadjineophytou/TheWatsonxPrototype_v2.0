# Unit Tests

This directory contains unit tests for the backend components of the Watson Prototype application.

## Purpose

Unit tests verify that individual components of the system work correctly in isolation. Each unit test focuses on a specific component and mocks all of its dependencies to ensure that only the component being tested is evaluated.

## Test Structure

Each test file corresponds to a specific component:

- `test_watson_client.py`: Tests for the Watson client
- `test_service_validator.py`: Tests for the service validator
- `test_text_service.py`: Tests for the text service
- `test_text_manager.py`: Tests for the text manager
- `test_iam_token_service.py`: Tests for the IAM token service
- `test_credentials_manager.py`: Tests for the credentials manager
- `test_service_factory.py`: Tests for the service factory
- `test_config_validator.py`: Tests for the config validator
- Additional test files will be added for other components

## Running Tests

To run the unit tests, use the following command from the project root:

```bash
pytest backend/tests/unit
```

To run a specific unit test file:

```bash
pytest backend/tests/unit/test_watson_client.py
```

## Writing Unit Tests

When writing unit tests, follow these guidelines:

1. Test one component at a time
2. Mock all dependencies of the component being tested
3. Test all public methods of the component
4. Test both success and error scenarios
5. Test edge cases and boundary conditions
6. Use descriptive test method names that describe the scenario being tested
7. Include docstrings for test classes and methods
8. Verify that exceptions are raised when expected
9. Verify that methods are called with the expected arguments
10. Verify that methods return the expected values

## Test Coverage

Aim for high test coverage (ideally 90% or higher) for each component. Use the coverage report to identify areas that need additional testing.

## Test Dependencies

The unit tests use the fixtures defined in the main `conftest.py` file. These fixtures provide mock objects that can be used across tests. 