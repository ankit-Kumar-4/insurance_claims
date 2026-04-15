#!/bin/bash

# Script to create initial Alembic migration
# This creates the database schema based on SQLAlchemy models

set -e

echo "======================================"
echo "Creating Initial Database Migration"
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

echo "Generating migration..."
alembic revision --autogenerate -m "Initial migration - create all tables"

echo ""
echo "✅ Migration created successfully!"
echo ""
echo "To apply the migration, run:"
echo "  alembic upgrade head"
echo ""
echo "To view migration status:"
echo "  alembic current"
echo ""
echo "To view migration history:"
echo "  alembic history"
