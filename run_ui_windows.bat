@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Running setup_windows.bat first...
    call setup_windows.bat
)

set PYTHONUTF8=1
echo ======================================================================
echo  Starting Bitcoin Web-of-Trust Interactive Dashboard
echo  Opening http://localhost:5000 in your default browser...
echo  (Press Ctrl+C in this window to stop the server)
echo ======================================================================
start "" "http://localhost:5000"
.venv\Scripts\python.exe src\serve.py 5000
pause
