@echo off
REM Project Scanner GUI - Portable Build Script
REM 이 배치 파일은 exe 파일을 생성합니다

echo [*] Building portable executable...
echo [*] This may take a few minutes...

cd /d %~dp0

REM 기존 build 폴더 삭제
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "gui_scanner.spec" del gui_scanner.spec

REM PyInstaller 실행
pyinstaller --name="ProjectScanner" ^
    --onefile ^
    --windowed ^
    --icon=scanner_icon.ico ^
    --add-data="src/project_scanner.py;src" ^
    --add-data="src/file_classifier.py;src" ^
    --add-data="src/analyzer.py;src" ^
    --add-data="src/detector.py;src" ^
    --add-data="src/visualizer.py;src" ^
    --add-data="src/reporter.py;src" ^
    --add-data="src/ground_truth_loader.py;src" ^
    --distpath=portable_build/bin ^
    --buildpath=build ^
    src/gui_scanner.py

if %ERRORLEVEL% EQU 0 (
    echo [+] Build successful!
    echo [+] Output: portable_build/bin/ProjectScanner.exe
) else (
    echo [!] Build failed. Check the output above.
)

pause
