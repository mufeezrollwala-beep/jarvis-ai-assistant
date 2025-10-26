# Testing Guide

This guide provides detailed information about the testing infrastructure for the Jarvis AI Assistant project.

## Test Suite Overview

The project includes a comprehensive test suite with:
- **33 unit and integration tests**
- **92%+ code coverage**
- **All external dependencies mocked**
- **Fast execution time (~2 seconds)**

## Test Structure

### Unit Tests (`tests/test_jarvis_unit.py`)

Unit tests verify individual methods in isolation:

- **TestJarvisInit**: Verifies Jarvis instance initialization
- **TestSpeak**: Tests text-to-speech functionality
- **TestWishMe**: Tests time-based greetings
- **TestTakeCommand**: Tests voice recognition
- **TestGetWikipediaSummary**: Tests Wikipedia integration
- **TestGetWeather**: Tests weather API integration
- **TestProcessCommand**: Tests command processing logic

### Integration Tests (`tests/test_jarvis_integration.py`)

Integration tests verify full command flows:

- **TestIntegrationWikipediaFlow**: Full Wikipedia query flow
- **TestIntegrationWeatherFlow**: Full weather query flow
- **TestIntegrationBrowserFlow**: Full browser command flow
- **TestIntegrationVoiceRecognitionFlow**: Voice to action flow
- **TestIntegrationErrorHandling**: Error handling across components
- **TestIntegrationGreetingFlow**: Greeting flow with time detection

### Test Fixtures (`tests/conftest.py`)

Shared fixtures for consistent test setup:

- `mock_pyttsx3_engine`: Mocks the TTS engine
- `mock_speech_recognizer`: Mocks the speech recognizer
- `mock_microphone`: Mocks microphone input
- `mock_wikipedia_summary`: Mocks Wikipedia API
- `mock_requests_get`: Mocks HTTP requests
- `mock_webbrowser_open`: Mocks browser opening

## Running Tests

### Basic Usage

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=jarvis --cov-report=html

# Run specific test file
pytest tests/test_jarvis_unit.py

# Run specific test class
pytest tests/test_jarvis_unit.py::TestSpeak

# Run specific test method
pytest tests/test_jarvis_unit.py::TestSpeak::test_speak_calls_engine_methods
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=jarvis --cov-report=html

# View the report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows

# Generate terminal coverage report with missing lines
pytest --cov=jarvis --cov-report=term-missing

# Generate XML coverage report (for CI tools)
pytest --cov=jarvis --cov-report=xml
```

### Testing Options

```bash
# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Run only failed tests from last run
pytest --lf

# Run failed tests first, then all others
pytest --ff

# Show slowest tests
pytest --durations=10
```

## Writing Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Unit Test

```python
from unittest.mock import Mock, patch
import pytest
from jarvis import Jarvis


class TestYourFeature:
    """Test your feature description"""

    @patch('jarvis.pyttsx3.init')
    def test_your_method(self, mock_pyttsx3_init):
        # Arrange: Setup mocks
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id='voice1')]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()

        # Act: Execute the method
        result = jarvis.your_method()

        # Assert: Verify the results
        assert result == expected_value
        mock_engine.say.assert_called_once()
```

### Example Integration Test

```python
from unittest.mock import Mock, MagicMock, patch
from jarvis import Jarvis


class TestIntegrationYourFlow:
    """Test your full flow description"""

    @patch('jarvis.external_dependency')
    @patch('jarvis.pyttsx3.init')
    def test_full_flow(self, mock_pyttsx3_init, mock_external):
        # Setup
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id='voice1')]
        mock_pyttsx3_init.return_value = mock_engine

        jarvis = Jarvis()

        # Execute full flow
        jarvis.method_one()
        result = jarvis.method_two()

        # Verify flow
        assert result is not None
        mock_external.assert_called()
```

### Using Fixtures

```python
def test_with_fixture(mock_pyttsx3_engine):
    # The fixture provides a pre-configured mock
    jarvis = Jarvis()
    # ... test code
```

## Mocking Strategy

### External Dependencies

All external dependencies are mocked to ensure:
- Tests run without hardware (microphone, speakers)
- Tests run without API keys
- Tests are fast and deterministic
- Tests can run in CI environment

### Mocked Components

1. **pyttsx3 (Text-to-Speech)**
   - `pyttsx3.init()`
   - `engine.say()`
   - `engine.runAndWait()`

2. **speech_recognition (Voice Recognition)**
   - `sr.Microphone()`
   - `recognizer.listen()`
   - `recognizer.recognize_google()`

3. **wikipedia**
   - `wikipedia.summary()`

4. **requests (HTTP)**
   - `requests.get()`
   - `response.json()`

5. **webbrowser**
   - `webbrowser.open()`

6. **datetime**
   - `datetime.datetime.now()`

## Coverage Goals

- **Target**: >80% code coverage on all modules
- **Current**: 92% coverage on jarvis.py
- **Focus**: Critical paths and edge cases

### Coverage by Module

```
jarvis.py    92%    Covers all core functionality
```

### Uncovered Lines

The 8% uncovered code consists of:
- Main execution loop (lines 121-127)
- Script entry point (line 131)

These are intentionally not tested as they represent the CLI entry point.

## Continuous Integration

### GitHub Actions Workflow

The CI pipeline runs on every push and pull request:

```yaml
- Test Stage: Runs on Python 3.8-3.12
- Lint Stage: Checks code quality
- Type Check Stage: Validates types
```

### CI Commands

The following commands run in CI:

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=jarvis --cov-report=xml --cov-fail-under=80

# Run linting
ruff check .

# Check formatting
black --check .

# Check imports
isort --check-only .

# Type checking
mypy jarvis.py
```

### Making CI Pass

Before pushing, ensure all checks pass locally:

```bash
# Run all checks
ruff check . && \
black --check . && \
isort --check-only . && \
mypy jarvis.py && \
pytest --cov=jarvis --cov-fail-under=80
```

## Common Testing Patterns

### Testing Time-Based Logic

```python
@patch('jarvis.datetime.datetime')
def test_time_based_feature(self, mock_datetime):
    mock_now = Mock()
    mock_now.hour = 14
    mock_datetime.now.return_value = mock_now
    # ... test code
```

### Testing Exception Handling

```python
def test_exception_handling(self):
    mock_api.side_effect = Exception("API error")
    result = jarvis.call_api()
    assert result is None
```

### Testing Exit Behavior

```python
def test_exit(self):
    with pytest.raises(SystemExit):
        jarvis.process_command("exit")
```

### Testing With Multiple Assertions

```python
def test_multiple_calls(self):
    jarvis.method()
    assert mock.call_count == 3
    mock.assert_any_call("First")
    mock.assert_any_call("Second")
```

## Troubleshooting

### Tests Fail with Import Errors

```bash
# Solution: Install in development mode
pip install -e .
```

### Coverage Below 80%

```bash
# View detailed coverage report
pytest --cov=jarvis --cov-report=html
open htmlcov/index.html

# Find uncovered lines and add tests
```

### Tests Pass Locally but Fail in CI

- Check Python version compatibility
- Ensure all dependencies are in requirements-dev.txt
- Check for OS-specific code
- Review CI logs for details

### Slow Tests

```bash
# Identify slow tests
pytest --durations=10

# Consider mocking slow operations
# Or marking slow tests with @pytest.mark.slow
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External Services**: Never call real APIs in tests
3. **Clear Test Names**: Names should describe what's being tested
4. **Arrange-Act-Assert**: Structure tests clearly
5. **Test Edge Cases**: Cover error conditions
6. **Keep Tests Fast**: Mock slow operations
7. **Maintain Coverage**: Add tests for new code
8. **Document Complex Tests**: Add comments for tricky setups

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

## Getting Help

- Review existing tests for examples
- Check CONTRIBUTING.md for development guidelines
- Open an issue for test-related questions
- Join discussions about testing strategies
