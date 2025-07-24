# glyphd Tests

This directory contains tests for the `glyphd` FastAPI service.

## Test Structure

- `conftest.py`: Contains shared pytest fixtures used across test files
- `test_api.py`: Tests for the FastAPI API endpoints
- `test_cli.py`: Tests for the CLI functionality

## Running Tests

To run all tests:

```bash
cd glyphd
python -m pytest
```

To run a specific test file:

```bash
cd glyphd
python -m pytest tests/test_api.py
```

To run a specific test:

```bash
cd glyphd
python -m pytest tests/test_api.py::test_health_endpoint
```

## Testing Approach

The tests in this directory follow the Test-Driven Development (TDD) approach, where tests are written before or alongside the implementation. The tests are designed to verify that the implementation meets the requirements without actually starting the server, which would block the process.

### API Testing

API tests use FastAPI's `TestClient`, which allows testing the API endpoints without actually starting the server. This is important because starting the server would block the process, making it difficult to run the tests in a CI/CD pipeline.

### CLI Testing

CLI tests use Click's `CliRunner`, which allows testing the CLI functionality without actually executing the commands. This is important because some commands, like the `serve` command, would start the server and block the process.

## Adding New Tests

When adding new tests, follow these guidelines:

1. Create a new test file if testing a new component
2. Use the fixtures from `conftest.py` where possible
3. Follow the naming convention: `test_*.py` for test files and `test_*` for test functions
4. Write tests that don't block the process (don't start the server)
5. Use FastAPI's `TestClient` for API tests and Click's `CliRunner` for CLI tests