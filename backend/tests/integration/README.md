# Integration Tests

This directory contains integration tests for the backend components of the Watson Prototype application.

## Purpose

Integration tests verify that different components of the system work together correctly. Unlike unit tests, which test individual components in isolation, integration tests examine the interactions between components and ensure they collaborate as expected.

## Test Structure

Each test file focuses on a specific flow or feature:

- `test_text_generation.py`: Tests the complete text generation flow from request to response
- Additional test files will be added for other features (NLU, speech, etc.)

## Running Tests

To run the integration tests, use the following command from the project root:

```bash
pytest backend/tests/integration
```

To run a specific integration test file:

```bash
pytest backend/tests/integration/test_text_generation.py
```

## Writing Integration Tests

When writing integration tests, follow these guidelines:

1. Focus on testing the interactions between components
2. Use real components where possible, mocking only external dependencies
3. Test complete flows from input to output
4. Verify that data is correctly passed between components
5. Test error handling and edge cases
6. Use descriptive test method names that describe the scenario being tested
7. Include docstrings for test classes and methods

## Test Dependencies

The integration tests use the same fixtures defined in the main `conftest.py` file. Additional fixtures specific to integration tests can be added to this directory if needed. 