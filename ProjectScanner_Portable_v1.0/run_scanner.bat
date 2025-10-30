@echo off
REM Project Scanner GUI - Portable Launcher
REM 이 파일을 클릭하여 프로젝트 스캐너를 실행하세요

cd /d %~dp0
echo [*] Starting Project Scanner...

if exist "bin\ProjectScanner.exe" (
    start "" "bin\ProjectScanner.exe"
) else (
    echo [!] Error: ProjectScanner.exe not found
    echo [*] Please run build_portable.bat first
    pause
)
