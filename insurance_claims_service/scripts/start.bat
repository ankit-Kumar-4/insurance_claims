@echo off
REM Quick start script for Windows (use after initial setup with run_local.bat)

echo Starting Insurance Claims API...

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo Error: Please run this script from the insurance_claims_service directory
    exit /b 1
)

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Success: Virtual environment activated
) else (
    echo Error: Virtual environment not found. Please run scripts\run_local.bat first
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo Error: .env file not found. Please run scripts\run_local.bat first
    exit /b 1
)

echo.
echo ==========================================
echo Application starting...
echo ==========================================
echo.
echo Available at:
echo   * API: http://localhost:8000
echo   * Docs: http://localhost:8000/docs
echo   * ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop
echo.

REM Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
