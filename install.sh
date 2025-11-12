#!/bin/bash
# Health Symptom Tracker - Installation Script

echo "Health Symptom Tracker - Installation"
echo "======================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

# Make tracker executable
chmod +x tracker.py
echo "Made tracker.py executable"

# Check if we should install dependencies
echo ""
read -p "Install dependencies (optional, only python-dateutil)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if we should use a virtual environment
    read -p "Create a virtual environment? (recommended) [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        echo "Virtual environment created"
    fi

    echo "Installing dependencies..."
    pip install -r requirements.txt

    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Installation failed. Please check the error messages above."
        exit 1
    fi
fi

echo ""
echo "Installation complete!"
echo ""
echo "Quick start:"
echo "  python tracker.py quick"
echo ""
echo "Or add a symptom directly:"
echo "  python tracker.py add -s \"Headache\" -S 7 -d \"Pain after work\""
echo ""
echo "For full documentation, see README.md"
