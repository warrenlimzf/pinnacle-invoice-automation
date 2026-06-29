@echo off
REM ===================================================================
REM  ONE-TIME SETUP (Windows). Double-click this once.
REM  Creates an isolated Python environment and installs the libraries.
REM ===================================================================
cd /d "%~dp0"

echo.
echo Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo  Python was not found. Install it first from https://www.python.org/downloads/
    echo  IMPORTANT: on the first install screen, tick "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

echo.
echo Creating virtual environment (.venv)...
python -m venv .venv

echo.
echo Installing libraries (this needs internet ONCE, only for the libraries -
echo  your client PDFs are never uploaded anywhere)...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ===================================================================
echo  Setup complete. You can now double-click  run_watcher.bat
echo ===================================================================
pause
