#!/bin/bash

echo "Running Jarvis AI Assistant Test Suite"
echo "======================================"

# Run all tests
python -m unittest discover -s tests -p "test_*.py" -v

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✓ All tests passed!"
else
    echo ""
    echo "✗ Some tests failed."
fi

exit $EXIT_CODE
