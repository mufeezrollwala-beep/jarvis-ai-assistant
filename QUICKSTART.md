# Quick Start Guide for Developers

This guide will get you up and running with the Jarvis AI Assistant development environment in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Git
- pip

## Setup (5 minutes)

### 1. Clone and Enter Directory

```bash
git clone <repository-url>
cd jarvis-ai-assistant
```

### 2. Run Setup Script (Automated)

```bash
bash scripts/setup.sh
```

**OR Manual Setup:**

```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements-dev.txt
```

### 3. Verify Installation

```bash
# Run tests
pytest

# Expected output: 33 passed, 92% coverage
```

## Essential Commands

### Testing
```bash
make test          # Run all tests
make coverage      # Run tests with HTML coverage report
pytest -v          # Verbose test output
```

### Code Quality
```bash
make format        # Auto-format code (black + isort)
make lint          # Check code quality
make typecheck     # Check types with mypy
make check         # Run ALL checks (recommended before commit)
```

### Development Workflow
```bash
make all           # Format, lint, typecheck, and test everything
```

## Project Structure

```
jarvis-ai-assistant/
├── jarvis.py           # Main code - your primary work file
├── tests/              # Test suite
│   ├── test_jarvis_unit.py         # Unit tests
│   └── test_jarvis_integration.py  # Integration tests
├── pyproject.toml      # All tool configurations
└── requirements-dev.txt # Dev dependencies
```

## Making Changes

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
Edit `jarvis.py` or other files

### 3. Add Tests
Add tests in `tests/test_jarvis_unit.py` or `tests/test_jarvis_integration.py`

### 4. Run Checks
```bash
make all  # This will format, lint, typecheck, and test
```

### 5. Commit
```bash
git add .
git commit -m "feat: your feature description"
```

### 6. Push and Create PR
```bash
git push origin feature/your-feature-name
```

## Common Tasks

### Add a New Feature

1. Write the code in `jarvis.py`
2. Write tests in `tests/test_jarvis_unit.py`
3. Run `make all` to verify
4. Ensure coverage stays >80%

### Fix a Bug

1. Write a failing test that demonstrates the bug
2. Fix the bug in `jarvis.py`
3. Verify the test passes
4. Run `make check`

### View Coverage Report

```bash
make coverage
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Troubleshooting

### "Command not found: make"

Use the direct commands:
```bash
pytest                    # instead of make test
black . && isort .        # instead of make format
```

### "Module not found"

```bash
source .venv/bin/activate  # Ensure venv is active
pip install -r requirements-dev.txt
```

### Tests Failing

```bash
pytest -v  # See detailed output
pytest -x  # Stop on first failure
pytest -s  # Show print statements
```

## Next Steps

- 📖 Read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
- 🧪 Read [TESTING.md](TESTING.md) for testing best practices
- 📝 Check [README.md](README.md) for project overview

## Getting Help

- Check existing tests for examples
- Review the documentation files
- Open an issue on GitHub

---

**That's it! You're ready to contribute! 🚀**
