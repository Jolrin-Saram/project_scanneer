@echo off
REM ============================================================================
REM YOLO Analysis Tool - Integrated Project Setup for Windows
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo  YOLO Analysis Tool - Integrated Project Setup
echo  Automated Discovery, Configuration ^& Environment Setup
echo ============================================================================
echo.

REM 현재 디렉토리 확인
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo [*] Setup Location: %SCRIPT_DIR%
echo [*] Running Python setup...
echo.

REM Python 버전 확인
python --version
if errorlevel 1 (
    echo [!] Python is not installed or not in PATH
    echo [*] Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo [*] Starting integrated setup process...
echo.

REM setup.py 실행
python "%SCRIPT_DIR%\setup.py"

if errorlevel 1 (
    echo.
    echo [!] Setup failed. Please review the errors above.
    pause
    exit /b 1
)

echo.
echo [+] Setup completed successfully!
echo.
echo Next steps:
echo 1. Activate virtual environment:
echo    %SCRIPT_DIR%\..\project_venv\Scripts\activate.bat
echo 2. Run YOLO analysis:
echo    python %SCRIPT_DIR%\main.py
echo.
pause
exit /b 0
