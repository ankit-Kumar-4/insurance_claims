#!/bin/bash

# Quick start script (use after initial setup with run_local.sh)

echo "Starting Insurance Claims API..."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "Error: Please run this script from the insurance_claims_service directory"
    exit 1
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "Error: Virtual environment not found. Please run ./scripts/run_local.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found. Please run ./scripts/run_local.sh first"
    exit 1
fi

echo ""
echo "=========================================="
echo "Application starting..."
echo "=========================================="
echo ""
echo "Available at:"
echo "  • API: http://localhost:8000"
echo "  • Docs: http://localhost:8000/docs"
echo "  • ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
