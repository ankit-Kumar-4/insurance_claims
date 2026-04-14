#!/bin/bash

# Insurance Claims Service - Local Development Script
# This script sets up and runs the application locally (without Docker)

set -e  # Exit on error

echo "=========================================="
echo "Insurance Claims Service - Local Setup"
echo "=========================================="

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if running from correct directory
if [ ! -f "app/main.py" ]; then
    print_error "Please run this script from the insurance_claims_service directory"
    exit 1
fi

# Step 1: Check Python version
echo ""
echo "Step 1: Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Step 2: Create virtual environment if it doesn't exist
echo ""
echo "Step 2: Setting up virtual environment..."
if [ ! -d "venv" ]; then
    print_warning "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Step 3: Activate virtual environment
echo ""
echo "Step 3: Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Step 4: Upgrade pip
echo ""
echo "Step 4: Upgrading pip..."
pip install --upgrade pip --quiet
print_success "Pip upgraded"

# Step 5: Install dependencies
echo ""
echo "Step 5: Installing dependencies..."
if [ -f "requirements.txt" ]; then
    print_warning "Installing production dependencies..."
    pip install -r requirements.txt --quiet
    print_success "Production dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

if [ -f "requirements-dev.txt" ]; then
    print_warning "Installing development dependencies..."
    pip install -r requirements-dev.txt --quiet
    print_success "Development dependencies installed"
fi

# Step 6: Set up environment variables
echo ""
echo "Step 6: Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warning ".env file created from .env.example"
        print_warning "⚠️  IMPORTANT: Edit .env file and set your SECRET_KEY and database credentials!"
        echo ""
        read -p "Press Enter to continue after editing .env file..."
    else
        print_error ".env.example not found"
        exit 1
    fi
else
    print_success ".env file already exists"
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Step 7: Check for PostgreSQL and Redis
echo ""
echo "Step 7: Checking required services..."

# Check PostgreSQL
if command -v psql &> /dev/null; then
    print_success "PostgreSQL client found"
    
    # Try to connect to PostgreSQL
    if psql -h localhost -U postgres -d postgres -c "SELECT 1;" &> /dev/null; then
        print_success "PostgreSQL is running"
    else
        print_warning "PostgreSQL is installed but not running or not accessible"
        echo "  You can start PostgreSQL manually or use: brew services start postgresql"
        echo "  Or start with Docker: docker-compose up -d postgres"
    fi
else
    print_warning "PostgreSQL not found"
    echo "  Option 1: Install PostgreSQL locally"
    echo "    macOS: brew install postgresql"
    echo "    Linux: sudo apt-get install postgresql"
    echo ""
    echo "  Option 2: Use Docker for PostgreSQL only"
    echo "    docker-compose up -d postgres"
fi

# Check Redis
if command -v redis-cli &> /dev/null; then
    print_success "Redis client found"
    
    # Try to connect to Redis
    if redis-cli ping &> /dev/null; then
        print_success "Redis is running"
    else
        print_warning "Redis is installed but not running"
        echo "  You can start Redis manually or use: brew services start redis"
        echo "  Or start with Docker: docker-compose up -d redis"
    fi
else
    print_warning "Redis not found"
    echo "  Option 1: Install Redis locally"
    echo "    macOS: brew install redis"
    echo "    Linux: sudo apt-get install redis"
    echo ""
    echo "  Option 2: Use Docker for Redis only"
    echo "    docker-compose up -d redis"
fi

# Step 8: Database setup
echo ""
echo "Step 8: Database setup..."
read -p "Do you want to run database migrations? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v alembic &> /dev/null; then
        print_warning "Running Alembic migrations..."
        alembic upgrade head
        print_success "Database migrations completed"
    else
        print_error "Alembic not found. Make sure dependencies are installed."
    fi
fi

# Step 9: Ask about test data
echo ""
echo "Step 9: Test data..."
read -p "Do you want to seed test data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "scripts/seed_data.py" ]; then
        print_warning "Seeding test data..."
        python scripts/seed_data.py
        print_success "Test data seeded"
    else
        print_warning "seed_data.py script not found (will be created in Phase 2)"
    fi
fi

# Step 10: Run the application
echo ""
echo "=========================================="
print_success "Setup complete! Starting application..."
echo "=========================================="
echo ""
echo "Application will be available at:"
echo "  • Main API: http://localhost:8000"
echo "  • Swagger UI: http://localhost:8000/docs"
echo "  • ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application with reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
