#!/bin/bash
# Setup script for Jarvis AI Assistant development environment

set -e

echo "🤖 Setting up Jarvis AI Assistant development environment..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION detected"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements-dev.txt -q

# Run initial tests
echo "🧪 Running tests..."
pytest -v

# Run code quality checks
echo "🔍 Running code quality checks..."
echo "  - ruff..."
ruff check .
echo "  - black..."
black --check .
echo "  - isort..."
isort --check-only .
echo "  - mypy..."
mypy jarvis.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Activate virtual environment: source .venv/bin/activate"
echo "   2. Run tests: pytest"
echo "   3. Run with coverage: pytest --cov=jarvis --cov-report=html"
echo "   4. Read CONTRIBUTING.md for development guidelines"
echo ""
echo "🚀 Happy coding!"
