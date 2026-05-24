@echo off
setlocal
cd /d "%~dp0"

call "%~dp0telepites.bat" --no-pause
if errorlevel 1 (
    echo.
    echo A telepites nem sikerult, ezert a program nem indul el.
    pause
    exit /b 1
)

echo.
echo Program inditasa...
".venv\Scripts\python.exe" main.py

echo.
pause
