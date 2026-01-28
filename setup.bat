@echo off
REM PDF Processor - Quick Start Script for Windows
REM This script automates the setup process

echo ==================================
echo PDF Processor - Quick Start Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or higher first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.

REM Success message
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo To use the PDF processor:
echo.
echo 1. Activate the environment:
echo    venv\Scripts\activate
echo.
echo 2. Run the processor:
echo    python pdf_processor.py input.pdf output.pdf
echo.
echo 3. (Optional) Set Claude API key for better results:
echo    set ANTHROPIC_API_KEY=your_key_here
echo.
echo See SETUP_GUIDE.md for detailed instructions!
echo.
pause