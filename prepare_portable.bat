@echo off
REM Portable Package Deployment Script

echo [*] Preparing portable package...

set PACKAGE_NAME=ProjectScanner_Portable_v1.0
set BUILD_DIR=portable_build
set DIST_DIR=%PACKAGE_NAME%

REM 기존 배포 폴더 정리
if exist %DIST_DIR% rmdir /s /q %DIST_DIR%

REM 배포 폴더 생성
mkdir %DIST_DIR%
mkdir %DIST_DIR%in
mkdir %DIST_DIR%\config
mkdir %DIST_DIR%\outputs
mkdir %DIST_DIR%\program_data

REM 필요한 파일 복사
echo [*] Copying files...
copy "build_portable.bat" "%DIST_DIR%\"
copy "run_scanner.bat" "%DIST_DIR%\"
copy "README_PORTABLE.md" "%DIST_DIR%\"
copy "scanner_icon.ico" "%DIST_DIR%\"
copy "portable_config.json" "%DIST_DIR%\"

REM 빌드된 exe 복사 (빌드 후)
if exist "%BUILD_DIR%in\ProjectScanner.exe" (
    copy "%BUILD_DIR%in\ProjectScanner.exe" "%DIST_DIR%in\"
    echo [+] Portable package ready!
    echo [+] Location: %DIST_DIR%
) else (
    echo [!] ProjectScanner.exe not found
    echo [*] Run build_portable.bat first
)

pause
