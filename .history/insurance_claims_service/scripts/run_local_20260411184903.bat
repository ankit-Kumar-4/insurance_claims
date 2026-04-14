@echo off
REM Insurance Claims Service - Local Development Script (Windows)
REM This script sets up and runs the application locally (without Docker)

echo ==========================================
echo Insurance Claims Service - Local Setup
echo ==========================================

REM Check if running from correct directory
if not exist "app\main.py" (
    echo Error: Please run this script from the insurance_claims_service directory
    exit /b 1
)

REM Step 1: Check Python version
echo.
echo Step 1: Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.11 or higher.
    exit /b 1
)
python --version
echo Success: Python found

REM Step 2: Create virtual environment if it doesn't exist
echo.
echo Step 2: Setting up virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Success: Virtual environment created
) else (
    echo Success: Virtual environment already exists
)

REM Step 3: Activate virtual environment
echo.
echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
echo Success: Virtual environment activated

REM Step 4: Upgrade pip
echo.
echo Step 4: Upgrading pip...
python -m pip install --upgrade pip --quiet
echo Success: Pip upgraded

REM Step 5: Install dependencies
echo.
echo Step 5: Installing dependencies...
if exist "requirements.txt" (
    echo Installing production dependencies...
    pip install -r requirements.txt --quiet
    echo Success: Production dependencies installed
) else (
    echo Error: requirements.txt not found
    exit /b 1
)

if exist "requirements-dev.txt" (
    echo Installing development dependencies...
    pip install -r requirements-dev.txt --quiet
    echo Success: Development dependencies installed
)

REM Step 6: Set up environment variables
echo.
echo Step 6: Setting up environment variables...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env
        echo Warning: .env file created from .env.example
        echo IMPORTANT: Edit .env file and set your SECRET_KEY and database credentials!
        echo.
        pause
    ) else (
        echo Error: .env.example not found
        exit /b 1
    )
) else (
    echo Success: .env file already exists
)

REM Step 7: Check for PostgreSQL and Redis
echo.
echo Step 7: Checking required services...

REM Check PostgreSQL
where psql >nul 2>&1
if %errorlevel% equ 0 (
    echo Success: PostgreSQL found
) else (
    echo Warning: PostgreSQL not found
    echo   Option 1: Install PostgreSQL locally
    echo   Option 2: Use Docker: docker-compose up -d postgres
)

REM Check Redis
where redis-cli >nul 2>&1
if %errorlevel% equ 0 (
    echo Success: Redis found
) else (
    echo Warning: Redis not found
    echo   Option 1: Install Redis locally
    echo   Option 2: Use Docker: docker-compose up -d redis
)

REM Step 8: Database setup
echo.
echo Step 8: Database setup...
set /p migrate="Do you want to run database migrations? (y/n): "
if /i "%migrate%"=="y" (
    where alembic >nul 2>&1
    if %errorlevel% equ 0 (
        echo Running Alembic migrations...
        alembic upgrade head
        echo Success: Database migrations completed
    ) else (
        echo Error: Alembic not found
    )
)

REM Step 9: Test data
echo.
echo Step 9: Test data...
set /p seed="Do you want to seed test data? (y/n): "
if /i "%seed%"=="y" (
    if exist "scripts\seed_data.py" (
        echo Seeding test data...
        python scripts\seed_data.py
        echo Success: Test data seeded
    ) else (
        echo Warning: seed_data.py script not found (will be created in Phase 2)
    )
)

REM Step 10: Run the application
echo.
echo ==========================================
echo Success: Setup complete! Starting application...
echo ==========================================
echo.
echo Application will be available at:
echo   * Main API: http://localhost:8000
echo   * Swagger UI: http://localhost:8000/docs
echo   * ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the application with reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
