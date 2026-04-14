#!/bin/bash

# Insurance Claims Service - Setup Script
echo "=========================================="
echo "Insurance Claims Service - Setup"
echo "=========================================="

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing production dependencies..."
pip install -r requirements.txt

echo ""
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Copy .env.example if .env doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and set your SECRET_KEY and other credentials!"
fi

# Start Docker services
echo ""
echo "Starting PostgreSQL and Redis with Docker..."
docker-compose up -d postgres redis

# Wait for services to be ready
echo ""
echo "Waiting for services to be ready..."
sleep 5

# Check Docker services
echo ""
echo "Checking Docker services..."
docker-compose ps

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and set SECRET_KEY and other credentials"
echo "2. Run migrations: alembic upgrade head"
echo "3. Start the application: uvicorn app.main:app --reload"
echo "4. Access Swagger UI: http://localhost:8000/docs"
echo ""
echo "For manual activation:"
echo "  source venv/bin/activate"
echo ""
