@echo off
setlocal
cd /d "%~dp0"

set "NO_PAUSE=%~1"
set "PYTHON_CMD="
set "PIP_DISABLE_PIP_VERSION_CHECK=1"

py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"

if not defined PYTHON_CMD (
    python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Python 3.9 vagy ujabb verzio nem talalhato ezen a gepen.
    echo Toltsd le innen: https://www.python.org/downloads/
    if not "%NO_PAUSE%"=="--no-pause" pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Virtualis kornyezet letrehozasa...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo Nem sikerult letrehozni a virtualis kornyezetet.
        if not "%NO_PAUSE%"=="--no-pause" pause
        exit /b 1
    )
)

echo Fuggosegek telepitese...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Nem sikerult telepiteni a fuggosegeket.
    if not "%NO_PAUSE%"=="--no-pause" pause
    exit /b 1
)

echo Telepites kesz.
if not "%NO_PAUSE%"=="--no-pause" pause
exit /b 0
