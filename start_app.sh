#!/bin/bash
echo "========================================"
echo "  Citizen Bot Pakistan - AI Assistant"
echo "========================================"
echo

echo "Activating virtual environment..."
source venv/bin/activate

echo
echo "Installing/updating dependencies..."
pip install -r requirements.txt

echo
echo "Starting the application..."
echo
echo "The application will be available at:"
echo "  http://localhost:5000"
echo
echo "Press Ctrl+C to stop the server"
echo

python app.py
