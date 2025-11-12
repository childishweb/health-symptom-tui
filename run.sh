#!/bin/bash
# Quick launcher for Health Symptom Tracker

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the application
python3 main.py

# Deactivate venv if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi
