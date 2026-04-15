#!/bin/bash

# Script to apply database migrations
# This runs all pending Alembic migrations

set -e

echo "======================================"
echo "Applying Database Migrations"
echo "======================================"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Warning: No virtual environment found. Make sure dependencies are installed."
fi

# Navigate to project directory
cd "$(dirname "$0")/.."

# Check current migration status
echo ""
echo "Current migration status:"
alembic current

echo ""
echo "Applying migrations..."
alembic upgrade head

echo ""
echo "✅ Migrations applied successfully!"
echo ""
echo "New migration status:"
alembic current

echo ""
echo "Migration history:"
alembic history --verbose
