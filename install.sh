#!/bin/bash
# Health Symptom Tracker - Installation Script

echo "🏥 Health Symptom Tracker - Installation"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Check if we should use a virtual environment
read -p "Create a virtual environment? (recommended) [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "To run the application:"
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  source venv/bin/activate"
    fi
    echo "  python main.py"
    echo ""
    echo "For help, see README.md"
else
    echo ""
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
