# Contributing to JARVIS

Thank you for your interest in contributing to JARVIS! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, trolling, or derogatory comments
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

1. Python 3.8 or higher
2. Git
3. Familiarity with voice assistants
4. Basic understanding of Python

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # On GitHub, click "Fork" button
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/jarvis-ai-assistant.git
   ```

4. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

6. **Verify installation**
   ```bash
   python jarvis.txt
   ```

## Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
# or
git checkout -b docs/your-documentation-change
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes

### 2. Make Your Changes

- Write clear, readable code
- Follow the coding standards (see below)
- Add comments for complex logic
- Update documentation as needed

### 3. Test Your Changes

Before committing:

```bash
# Run manual tests
python jarvis.txt

# Test specific skills
python -c "from examples.calculator_skill import CalculatorSkill; # test code"

# Run unit tests (if available)
pytest tests/

# Check code style
flake8 *.py
black --check *.py
```

### 4. Commit Your Changes

Write meaningful commit messages:

```bash
git add .
git commit -m "feat: add calculator skill with safe evaluation"
```

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build process or auxiliary tool changes

**Examples:**
```
feat: add news headlines skill

Implements NewsAPI integration to fetch and read top headlines.
Supports category and country filtering.

Closes #123
```

```
fix: correct weather temperature conversion

The temperature was incorrectly calculated in Fahrenheit.
Now properly converts from Kelvin to Celsius.

Fixes #456
```

### 5. Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

### 6. Push Your Changes

```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions and classes

### Code Formatting

Use `black` for automatic formatting:

```bash
black jarvis.txt
black examples/*.py
```

### Linting

Use `flake8` for linting:

```bash
flake8 jarvis.txt --max-line-length=100
```

### Documentation

- Every function should have a docstring
- Use Google-style docstrings

```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Longer description if needed, explaining what the function does,
    any important details, or edge cases.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
    
    Returns:
        type: Description of return value
    
    Raises:
        ExceptionType: When and why this exception is raised
    
    Example:
        >>> function_name("test", 123)
        "result"
    """
    # Implementation
    pass
```

### Naming Conventions

- **Variables**: `lowercase_with_underscores`
- **Functions**: `lowercase_with_underscores()`
- **Classes**: `CamelCase`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private methods**: `_leading_underscore()`

### Example Good Code

```python
class WeatherSkill:
    """Fetch weather information from OpenWeatherMap API."""
    
    def __init__(self, jarvis_instance):
        """
        Initialize weather skill.
        
        Args:
            jarvis_instance: Reference to main Jarvis instance
        """
        self.jarvis = jarvis_instance
        self.api_key = self._get_api_key()
    
    def can_handle(self, query):
        """
        Check if this skill can handle the query.
        
        Args:
            query (str): User's voice command
        
        Returns:
            bool: True if skill can handle this query
        """
        return 'weather' in query.lower()
    
    def _get_api_key(self):
        """Get API key from configuration."""
        return self.jarvis.config.get('apis', {}).get('openweathermap', {}).get('api_key')
```

## Pull Request Process

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if applicable)
- [ ] No new warnings generated
- [ ] Tests pass (if applicable)
- [ ] Commit messages follow conventions

### Submitting Pull Request

1. **Push your branch to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open Pull Request on GitHub**
   - Go to your fork on GitHub
   - Click "Pull Request" button
   - Select your branch
   - Fill in the PR template

3. **PR Title and Description**

   **Title format:**
   ```
   [Type] Brief description
   ```

   **Description should include:**
   - What changes were made
   - Why these changes were needed
   - How to test the changes
   - Related issues (if any)

   **Example:**
   ```markdown
   ## Description
   Adds a calculator skill that safely evaluates mathematical expressions.
   
   ## Changes
   - Created `CalculatorSkill` class
   - Implemented safe evaluation using AST
   - Added natural language parsing for operators
   - Added example usage in `examples/`
   
   ## Testing
   - Tested with basic arithmetic operations
   - Tested with complex expressions
   - Verified safety against code injection
   
   ## Related Issues
   Closes #42
   ```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

### After Merge

- Delete your feature branch
- Update your fork:
  ```bash
  git checkout main
  git pull upstream main
  git push origin main
  ```

## Reporting Bugs

### Before Submitting a Bug Report

- Check existing issues to avoid duplicates
- Collect information about the bug
- Verify it's reproducible

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run JARVIS
2. Say "..."
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Screenshots/Logs**
If applicable, add screenshots or error logs.

**Environment:**
 - OS: [e.g. Windows 10, macOS 12, Ubuntu 20.04]
 - Python Version: [e.g. 3.10.2]
 - JARVIS Version: [e.g. 1.0.0]

**Additional context**
Any other relevant information.
```

## Suggesting Enhancements

### Before Submitting an Enhancement

- Check if the enhancement has already been suggested
- Determine if it fits the project scope
- Provide a clear use case

### Enhancement Suggestion Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions or features you've considered.

**Additional context**
Mockups, examples, or other relevant information.

**Use cases**
Real-world scenarios where this would be useful.
```

## Types of Contributions

### 1. New Skills

Create new capabilities for JARVIS:

- Research and implement API integrations
- Create natural language command handlers
- Write tests and documentation
- Add examples

See [Skill Authoring Guide](docs/skill-authoring.md).

### 2. Bug Fixes

Help make JARVIS more stable:

- Fix reported issues
- Improve error handling
- Add validation
- Optimize performance

### 3. Documentation

Improve documentation:

- Fix typos or unclear explanations
- Add examples and tutorials
- Create diagrams
- Translate documentation

### 4. Testing

Improve test coverage:

- Write unit tests
- Add integration tests
- Create test fixtures
- Improve test documentation

### 5. Design and UX

Improve user experience:

- Design GUI mockups
- Improve voice responses
- Enhance error messages
- Create visual diagrams

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in documentation

## Questions?

- Open an issue for questions
- Check documentation in `docs/`
- Join discussions on GitHub

---

Thank you for contributing to JARVIS! 🚀
