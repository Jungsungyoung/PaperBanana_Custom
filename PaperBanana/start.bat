@echo off
chcp 65001 >nul
REM ============================================================================
REM PaperBanana Streamlit Launcher (Windows)
REM ============================================================================
REM This script launches the PaperBanana Streamlit demo.
REM Prerequisites: Run setup.bat first to set up the environment.
REM ============================================================================

echo.
echo ============================================================================
echo Starting PaperBanana Streamlit Demo
echo ============================================================================
echo.

REM Activate virtual environment
echo [1/2] Activating Python virtual environment...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo Error: Failed to activate virtual environment
    echo Solution: Run setup.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM Run Streamlit
echo [2/2] Starting Streamlit demo...
echo.
echo Browser will open automatically. (default: http://localhost:8501)
echo Press Ctrl+C to exit.
echo.

.venv\Scripts\python -m streamlit run demo.py

if errorlevel 1 (
    echo.
    echo Error: Streamlit execution failed
    echo Solutions:
    echo   1. Check if requirements.txt is installed
    echo   2. Try running setup.bat again
    echo.
    pause
    exit /b 1
)

pause
