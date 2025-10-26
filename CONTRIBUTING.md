# Contributing to Jarvis AI Assistant

Thank you for your interest in contributing to the Jarvis AI Assistant project! This guide will help you get started with development and testing.

## Table of Contents

- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Code Quality](#code-quality)
- [Adding New Tests](#adding-new-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Pull Request Process](#pull-request-process)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements-dev.txt
```

4. (Optional) Set up pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

This will automatically run code quality checks before each commit.

5. Install system dependencies (Linux/Ubuntu):
```bash
sudo apt-get install portaudio19-dev python3-pyaudio espeak
```

On macOS:
```bash
brew install portaudio espeak
```

## Running Tests

### Run All Tests

To run the complete test suite:

```bash
pytest
```

### Run Tests with Coverage

To run tests and generate a coverage report:

```bash
pytest --cov=jarvis --cov-report=html --cov-report=term-missing
```

View the HTML coverage report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

### Run Specific Tests

Run unit tests only:
```bash
pytest tests/test_jarvis_unit.py
```

Run integration tests only:
```bash
pytest tests/test_jarvis_integration.py
```

Run a specific test class:
```bash
pytest tests/test_jarvis_unit.py::TestSpeak
```

Run a specific test method:
```bash
pytest tests/test_jarvis_unit.py::TestSpeak::test_speak_calls_engine_methods
```

### Run Tests in Verbose Mode

```bash
pytest -v
```

### Run Tests with Print Statements

```bash
pytest -s
```

## Code Quality

This project uses several tools to maintain code quality:

### Linting with Ruff

Check for code issues:
```bash
ruff check .
```

Auto-fix issues where possible:
```bash
ruff check --fix .
```

### Code Formatting with Black

Check formatting:
```bash
black --check .
```

Auto-format code:
```bash
black .
```

### Import Sorting with isort

Check import order:
```bash
isort --check-only .
```

Auto-sort imports:
```bash
isort .
```

### Type Checking with mypy

Run type checking:
```bash
mypy jarvis.py
```

### Run All Quality Checks

Run all quality checks at once:
```bash
ruff check . && black --check . && isort --check-only . && mypy jarvis.py && pytest
```

## Adding New Tests

### Test Structure

Tests are organized in the `tests/` directory:

- `tests/conftest.py` - Shared fixtures and test configuration
- `tests/test_jarvis_unit.py` - Unit tests for individual methods
- `tests/test_jarvis_integration.py` - Integration tests for full flows

### Writing Unit Tests

Unit tests should test individual methods in isolation using mocks:

```python
from unittest.mock import Mock, patch
import pytest
from jarvis import Jarvis


class TestYourFeature:
    """Test description"""
    
    @patch('jarvis.pyttsx3.init')
    def test_your_method(self, mock_pyttsx3_init):
        # Setup
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id='voice1')]
        mock_pyttsx3_init.return_value = mock_engine
        
        jarvis = Jarvis()
        
        # Execute
        result = jarvis.your_method()
        
        # Assert
        assert result == expected_value
```

### Writing Integration Tests

Integration tests should test multiple components working together:

```python
from unittest.mock import Mock, MagicMock, patch
from jarvis import Jarvis


class TestIntegrationYourFlow:
    """Test full flow description"""
    
    @patch('jarvis.external_dependency')
    @patch('jarvis.pyttsx3.init')
    def test_full_flow(self, mock_pyttsx3_init, mock_external):
        # Setup mocks
        mock_engine = MagicMock()
        mock_engine.getProperty.return_value = [Mock(id='voice1')]
        mock_pyttsx3_init.return_value = mock_engine
        
        jarvis = Jarvis()
        
        # Test the full flow
        jarvis.method_one()
        result = jarvis.method_two()
        
        # Verify the flow
        assert result is not None
        mock_external.assert_called()
```

### Using Fixtures

Reusable test fixtures are defined in `tests/conftest.py`:

```python
def test_with_fixture(mock_pyttsx3_engine):
    # Use the fixture
    jarvis = Jarvis()
    # ... test code
```

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Use descriptive names that explain what is being tested

### Coverage Goals

- Aim for >80% coverage on core modules
- Focus on testing critical paths and edge cases
- Mock external dependencies (APIs, hardware, etc.)

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration. The CI pipeline runs on every push and pull request.

### CI Pipeline Stages

1. **Test Stage** - Runs on Python 3.8, 3.9, 3.10, 3.11, and 3.12
   - Installs dependencies
   - Runs pytest with coverage
   - Uploads coverage reports to Codecov

2. **Lint Stage** - Checks code quality
   - Runs ruff for linting
   - Checks black formatting
   - Checks isort import ordering

3. **Type Check Stage** - Validates type annotations
   - Runs mypy type checker

### Viewing CI Results

CI results are visible in:
- Pull request checks
- GitHub Actions tab
- Commit status badges

### Local CI Simulation

Run the same checks locally before pushing:

```bash
# Run linting
ruff check .
black --check .
isort --check-only .

# Run type checking
mypy jarvis.py

# Run tests with coverage
pytest --cov=jarvis --cov-fail-under=80
```

## Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write Code and Tests**
   - Implement your changes
   - Add/update tests
   - Ensure coverage stays above 80%

3. **Run Quality Checks**
   ```bash
   # Format code
   black .
   isort .
   
   # Check for issues
   ruff check .
   mypy jarvis.py
   
   # Run tests
   pytest
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub and create a pull request
   - Fill in the PR template
   - Wait for CI checks to pass
   - Request review from maintainers

7. **Address Review Feedback**
   - Make requested changes
   - Push updates to the same branch
   - CI will automatically re-run

### Commit Message Format

Follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks

### PR Requirements

- All CI checks must pass (tests, lint, type check)
- Code coverage must be >80%
- Code must be formatted with black and isort
- Changes must include tests
- Documentation must be updated if needed

## Troubleshooting

### Common Issues

**Issue: Tests fail with "No module named 'jarvis'"**
```bash
# Solution: Install the package in development mode
pip install -e .
```

**Issue: PyAudio installation fails**
```bash
# Linux/Ubuntu
sudo apt-get install portaudio19-dev python3-pyaudio

# macOS
brew install portaudio

# Then reinstall
pip install pyaudio
```

**Issue: pyttsx3 fails on Linux**
```bash
# Install espeak
sudo apt-get install espeak
```

**Issue: Coverage below 80%**
- Add tests for uncovered code paths
- Check coverage report: `pytest --cov-report=html`
- View `htmlcov/index.html` to see uncovered lines

## Getting Help

- Open an issue on GitHub for bugs
- Start a discussion for questions
- Check existing issues and discussions first

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming and inclusive community.

## License

By contributing, you agree that your contributions will be licensed under the project's license.
