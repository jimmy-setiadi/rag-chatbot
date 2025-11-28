# RAG System Testing Framework

## Overview
Enhanced testing framework for the RAG system with comprehensive API endpoint testing, pytest configuration, and shared fixtures.

## Test Structure

### Test Categories
- **Unit Tests** (`@pytest.mark.unit`): Individual component testing
- **Integration Tests** (`@pytest.mark.integration`): Component interaction testing  
- **API Tests** (`@pytest.mark.api`): FastAPI endpoint testing

### Key Files
- `conftest.py` - Shared fixtures and test configuration
- `test_api_endpoints.py` - API endpoint tests
- `test_integration_api.py` - API integration tests
- `run_tests.py` - Test runner script

## Running Tests

### Using pytest directly:
```bash
# All tests
pytest

# Specific test categories
pytest -m unit
pytest -m api
pytest -m integration

# Specific test file
pytest tests/test_api_endpoints.py

# Verbose output
pytest -v
```

### Using test runner script:
```bash
# All tests
python run_tests.py

# Specific categories
python run_tests.py unit
python run_tests.py api
python run_tests.py integration

# With coverage
python run_tests.py coverage
```

## Test Fixtures

### `mock_config`
Mock configuration object for testing without real API keys or database connections.

### `mock_rag_system`
Mock RAG system with predefined responses for API testing.

### `test_client`
FastAPI TestClient with mocked dependencies, avoiding static file mounting issues.

### `sample_query_data` / `sample_course_data`
Sample data structures for consistent testing.

## API Test Coverage

### Endpoints Tested:
- `POST /api/query` - Query processing
- `GET /api/courses` - Course statistics
- `POST /api/new-session` - Session creation
- `GET /api/commands` - Available commands

### Test Scenarios:
- Successful requests/responses
- Error handling
- Request validation
- Response format validation
- CORS configuration
- Session management

## Configuration

Pytest configuration in `pyproject.toml`:
- Test discovery patterns
- Async test support
- Custom markers
- Output formatting

## Dependencies

Required packages (added to pyproject.toml):
- `pytest` - Testing framework
- `httpx` - HTTP client for FastAPI testing
- `pytest-asyncio` - Async test support