# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive testing suite with pytest
  - 33 unit and integration tests
  - 92%+ code coverage
  - All external dependencies mocked
- Code quality tools configuration
  - Ruff for linting
  - Black for code formatting
  - isort for import sorting
  - mypy for type checking
- GitHub Actions CI/CD pipeline
  - Test stage (Python 3.8-3.12)
  - Lint stage
  - Type check stage
- Developer documentation
  - CONTRIBUTING.md with setup and workflow guidelines
  - TESTING.md with comprehensive testing guide
  - README.md expanded with usage examples
- Development tooling
  - Makefile with common commands
  - setup.sh script for automated setup
  - .pre-commit-config.yaml for pre-commit hooks
  - Pull request template
- Type hints throughout codebase
- .gitignore file

### Changed
- Refactored jarvis.txt to jarvis.py
- Improved code organization with proper typing
- Enhanced error handling with Optional return types
- Extracted weather and Wikipedia logic into separate methods

### Fixed
- All linting and formatting issues resolved
- Type checking passes with mypy
- Code follows PEP 8 style guide

## [0.1.0] - Initial Release

### Added
- Basic Jarvis voice assistant functionality
- Voice recognition with speech_recognition
- Text-to-speech with pyttsx3
- Wikipedia integration
- Weather API integration (OpenWeatherMap)
- Browser control (YouTube, Google)
- Time reporting
- Exit command handling
