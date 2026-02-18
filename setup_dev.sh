#!/bin/bash
# Setup script for OpenClaw-Sentinel developers

echo "Setting up development environment for OpenClaw-Sentinel..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Install dependencies
source venv/bin/activate
pip install pyyaml psutil

echo "--------------------------------------------------"
echo "Module Assignment:"
echo "- Sentinel-Guard: Core engine implemented (Policy & Filtering)."
echo "- Sentinel-Audit: Basic logging implemented."
echo "- Sentinel-Pulse: Feb, please extend pulse.py for advanced monitoring."
echo "- Sentinel-Masking: Mar, please extend masking.py for complex PII rules."
echo "--------------------------------------------------"
echo "To start development:"
echo "source venv/bin/activate"
echo "python sentinel_guard/guard.py"
echo "python sentinel_pulse/pulse.py"
echo "python sentinel_masking/masking.py"
