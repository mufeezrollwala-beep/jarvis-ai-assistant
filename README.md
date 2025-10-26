# jarvis-ai-assistant

Advanced AI assistant inspired by Iron Man's JARVIS

[![CI](https://github.com/yourusername/jarvis-ai-assistant/workflows/CI/badge.svg)](https://github.com/yourusername/jarvis-ai-assistant/actions)
[![codecov](https://codecov.io/gh/yourusername/jarvis-ai-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/jarvis-ai-assistant)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

- 🎤 Voice recognition and command processing
- 🗣️ Text-to-speech responses
- 📚 Wikipedia integration for knowledge queries
- 🌐 Web browser control (YouTube, Google)
- ⏰ Time reporting
- 🌤️ Weather information (OpenWeatherMap API)
- 🧪 Comprehensive test suite with >80% coverage
- 🔍 Automated code quality checks (linting, formatting, type checking)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### System Dependencies

**Linux/Ubuntu:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio espeak
```

**macOS:**
```bash
brew install portaudio espeak
```

**Windows:**
- PyAudio: Download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- eSpeak: Download from [here](http://espeak.sourceforge.net/download.html)

### Install Package

```bash
# Clone the repository
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from jarvis import Jarvis

# Create Jarvis instance
jarvis = Jarvis()

# Greet the user
jarvis.wish_me()

# Process voice commands
while True:
    command = jarvis.take_command()
    if command != 'None':
        jarvis.process_command(command)
```

### Run as Script

```bash
python jarvis.py
```

### Supported Commands

- **"Wikipedia [topic]"** - Search Wikipedia for information
- **"Open YouTube"** - Open YouTube in browser
- **"Open Google"** - Open Google in browser
- **"What time is it"** - Get current time
- **"What's the weather"** - Get weather information (requires API key)
- **"Exit"** - Exit the assistant

### Weather API Setup

To use weather functionality:

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Configure when calling `process_command()`:

```python
jarvis.process_command(
    command,
    weather_api_key="your_api_key_here",
    city="your_city_name"
)
```

## Development

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=jarvis --cov-report=html

# Run specific test file
pytest tests/test_jarvis_unit.py

# Run specific test class
pytest tests/test_jarvis_unit.py::TestSpeak
```

### Code Quality

```bash
# Run linting
ruff check .

# Format code
black .

# Sort imports
isort .

# Type checking
mypy jarvis.py

# Run all checks
ruff check . && black --check . && isort --check-only . && mypy jarvis.py && pytest
```

### Project Structure

```
jarvis-ai-assistant/
├── jarvis.py              # Main application code
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Shared test fixtures
│   ├── test_jarvis_unit.py       # Unit tests
│   └── test_jarvis_integration.py # Integration tests
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI configuration
├── pyproject.toml        # Project configuration
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── README.md            # This file
└── CONTRIBUTING.md      # Developer guide
```

## Testing

The project includes a comprehensive test suite with:

- **Unit tests**: Test individual methods in isolation
- **Integration tests**: Test full command flows
- **Mocked dependencies**: All external dependencies are mocked
- **Coverage tracking**: Maintains >80% code coverage
- **Automated CI**: Tests run automatically on every PR

### Test Coverage

Current coverage: >80% on core modules

View detailed coverage report:
```bash
pytest --cov=jarvis --cov-report=html
open htmlcov/index.html
```

## CI/CD

The project uses GitHub Actions for continuous integration:

- **Test Stage**: Runs tests on Python 3.8-3.12
- **Lint Stage**: Checks code quality with ruff, black, isort
- **Type Check Stage**: Validates type annotations with mypy

All checks must pass before merging pull requests.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Setting up development environment
- Running tests locally
- Code quality standards
- Pull request process

## License

This project is licensed under the MIT License.

## Acknowledgments

- Inspired by Iron Man's JARVIS
- Built with Python and various open-source libraries
- Special thanks to all contributors

## Support

- 📝 Report bugs via [GitHub Issues](https://github.com/yourusername/jarvis-ai-assistant/issues)
- 💬 Ask questions in [GitHub Discussions](https://github.com/yourusername/jarvis-ai-assistant/discussions)
- 📧 Contact: your.email@example.com

## Roadmap

- [ ] Add more voice commands
- [ ] Integrate additional APIs (news, calendar, etc.)
- [ ] Support for multiple languages
- [ ] Web interface
- [ ] Mobile app integration
- [ ] Plugin system for extensions
