@echo off
setlocal
cd /d "%~dp0"

echo ======================================================================
echo  Bitcoin Web-of-Trust Link Prediction - Windows Environment Setup
echo ======================================================================

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not found in your PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo and check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating virtual environment in .venv ...
    python -m venv .venv
) else (
    echo [1/3] Virtual environment .venv already exists.
)

echo [2/3] Installing required packages from requirements.txt ...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt

echo [3/3] Running automated test suite to verify setup ...
set PYTHONUTF8=1
.venv\Scripts\python.exe run.py test

echo ======================================================================
echo  Setup complete! To launch the interactive Web UI, run:
echo      run_ui_windows.bat
echo  Or from PowerShell / CMD:
echo      .venv\Scripts\python.exe run.py serve
echo ======================================================================
pause
