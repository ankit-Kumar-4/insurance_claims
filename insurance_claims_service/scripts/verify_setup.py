#!/usr/bin/env python3
"""
Quick verification script to test if the basic setup is working.
Run this before starting the application to verify all imports work.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all basic imports work"""
    print("Testing basic imports...")
    
    try:
        print("  ✓ Importing FastAPI...", end=" ")
        from fastapi import FastAPI
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False
    
    try:
        print("  ✓ Importing SQLAlchemy...", end=" ")
        from sqlalchemy import create_engine
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False
    
    try:
        print("  ✓ Importing Pydantic...", end=" ")
        from pydantic import BaseModel
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False
    
    try:
        print("  ✓ Importing app.config...", end=" ")
        from app.config import settings
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False
    
    try:
        print("  ✓ Importing app.database...", end=" ")
        from app.database import engine
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False
    
    try:
        print("  ✓ Importing app.models.base...", end=" ")
        from app.models.base import Base, BaseModel
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False
    
    try:
        print("  ✓ Importing app.main...", end=" ")
        from app.main import app
        print("OK")
    except ImportError as e:
        print(f"FAILED: {e}")
        return False
    
    return True


def test_config():
    """Test that configuration is loaded"""
    print("\nTesting configuration...")
    
    try:
        from app.config import settings
        print(f"  ✓ APP_NAME: {settings.APP_NAME}")
        print(f"  ✓ DEBUG: {settings.DEBUG}")
        print(f"  ✓ ENVIRONMENT: {settings.ENVIRONMENT}")
        
        # Check if SECRET_KEY is set
        if settings.SECRET_KEY == "your-secret-key-change-this-in-production-min-32-chars":
            print("  ⚠️  WARNING: SECRET_KEY is still default value!")
            print("     Please update SECRET_KEY in .env file")
        else:
            print(f"  ✓ SECRET_KEY is set (length: {len(settings.SECRET_KEY)} chars)")
        
        return True
    except Exception as e:
        print(f"  ✗ Configuration test failed: {e}")
        return False


def test_database_models():
    """Test that database models can be imported"""
    print("\nTesting database models...")
    
    try:
        from app.models.base import Base, BaseModel
        print(f"  ✓ Base class: {Base}")
        print(f"  ✓ BaseModel class: {BaseModel}")
        return True
    except Exception as e:
        print(f"  ✗ Models test failed: {e}")
        return False


def main():
    """Run all verification tests"""
    print("="*50)
    print("Insurance Claims API - Setup Verification")
    print("="*50)
    print()
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test config
    if not test_config():
        all_passed = False
    
    # Test models
    if not test_database_models():
        all_passed = False
    
    print()
    print("="*50)
    if all_passed:
        print("✅ All verification tests passed!")
        print("="*50)
        print()
        print("You can now start the application with:")
        print("  uvicorn app.main:app --reload")
        print()
        print("Or use the quick start script:")
        print("  ./scripts/start.sh")
        return 0
    else:
        print("❌ Some verification tests failed!")
        print("="*50)
        print()
        print("Please check the errors above and fix them before running the application.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
