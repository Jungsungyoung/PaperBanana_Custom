@echo off
chcp 65001 >nul
REM ============================================================================
REM PaperBanana Setup Script (Windows)
REM ============================================================================
REM This script sets up the initial environment for PaperBanana:
REM   1. Check uv installation
REM   2. Create Python virtual environment
REM   3. Install required packages
REM   4. Copy configuration files
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo PaperBanana Initial Setup
echo ============================================================================
echo.

REM Check uv installation
echo [1/4] Checking uv installation...
where uv >nul 2>&1

if errorlevel 1 (
    echo.
    echo Error: uv is not installed.
    echo.
    echo Solution:
    echo   1. Visit https://docs.astral.sh/uv/getting-started/installation/
    echo   2. Download and run the Windows uv installer
    echo   3. Run this script again after installation
    echo.
    pause
    exit /b 1
)

echo uv installation verified!
echo.

REM Create virtual environment
echo [2/4] Creating Python virtual environment...

if exist .venv (
    echo Virtual environment already exists. Using existing environment.
) else (
    uv venv
    
    if errorlevel 1 (
        echo.
        echo Error: Failed to create virtual environment
        echo.
        pause
        exit /b 1
    )
    
    echo Virtual environment created successfully!
)

echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment and installing packages...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo Error: Failed to activate virtual environment
    echo.
    pause
    exit /b 1
)

REM Install packages
uv pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Package installation failed
    echo.
    echo Solutions:
    echo   1. Check if requirements.txt exists
    echo   2. Check your internet connection
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Package installation complete!
echo.

REM Copy configuration file
echo [4/4] Copying configuration files...

if exist configs\model_config.yaml (
    echo Configuration file already exists. Keeping existing file.
) else (
    if exist configs\model_config.template.yaml (
        copy configs\model_config.template.yaml configs\model_config.yaml
        
        if errorlevel 1 (
            echo.
            echo Warning: Failed to copy configuration file
            echo Please manually run:
            echo   copy configs\model_config.template.yaml configs\model_config.yaml
            echo.
        ) else (
            echo Configuration file copied successfully!
        )
    ) else (
        echo.
        echo Warning: model_config.template.yaml file not found.
        echo.
    )
)

echo.
echo ============================================================================
echo Setup Complete!
echo ============================================================================
echo.
echo Next Steps:
echo   1. Open configs/model_config.yaml and configure your API keys:
echo      - defaults.model_name: Model name (e.g., gemini-3-pro-preview)
echo      - defaults.image_model_name: Image generation model name
echo      - api_keys: Enter required API keys
echo.
echo   2. Run the Streamlit demo with:
echo      start.bat
echo.
echo   Or run directly from command line:
echo      streamlit run demo.py
echo.
pause
