## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🧪 Test improvements
- [ ] 🔧 Configuration changes

## Checklist

- [ ] I have read the [CONTRIBUTING.md](../CONTRIBUTING.md) guidelines
- [ ] My code follows the code style of this project
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass locally
- [ ] I have updated the documentation accordingly
- [ ] My changes generate no new warnings
- [ ] I have checked my code with the linters (ruff, black, isort)
- [ ] I have run type checking (mypy)
- [ ] Test coverage is maintained at >80%

## Testing

<!-- Describe the tests you ran to verify your changes -->

```bash
# Commands used for testing
pytest -v
pytest --cov=jarvis --cov-report=term-missing
```

**Test Coverage:** <!-- e.g., 92% -->

## Code Quality Checks

```bash
# Run these commands before submitting
make check
# or
ruff check . && black --check . && isort --check-only . && mypy jarvis.py && pytest
```

- [ ] All linting checks pass
- [ ] Code is formatted with black and isort
- [ ] Type checking passes with mypy
- [ ] All tests pass with coverage >80%

## Related Issues

<!-- Link any related issues here -->
Closes #
Relates to #

## Screenshots (if applicable)

<!-- Add screenshots here if your changes affect the UI or output -->

## Additional Notes

<!-- Any additional information that reviewers should know -->
