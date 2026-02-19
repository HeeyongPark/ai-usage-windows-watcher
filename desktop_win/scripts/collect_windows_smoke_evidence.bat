@echo off
setlocal

set "BASE_DIR=%~dp0"
set "PREPARE_SCRIPT=%BASE_DIR%prepare_windows_smoke_evidence.ps1"
set "APP_EXE=%BASE_DIR%AIUsageWatcher.exe"

if not exist "%PREPARE_SCRIPT%" (
  echo [ERROR] prepare_windows_smoke_evidence.ps1 not found:
  echo         %PREPARE_SCRIPT%
  echo.
  echo This helper must be placed in the AIUsageWatcher bundle folder.
  pause
  exit /b 1
)

if not exist "%APP_EXE%" (
  echo [ERROR] AIUsageWatcher.exe not found in:
  echo         %BASE_DIR%
  echo.
  echo Run this script from the onedir bundle root.
  pause
  exit /b 1
)

set "RUN_ID=%~1"
if defined RUN_ID (
  powershell -ExecutionPolicy Bypass -File "%PREPARE_SCRIPT%" -BundleRoot "%BASE_DIR%" -RunId "%RUN_ID%"
) else (
  powershell -ExecutionPolicy Bypass -File "%PREPARE_SCRIPT%" -BundleRoot "%BASE_DIR%"
)

if not "%ERRORLEVEL%"=="0" (
  echo [ERROR] Evidence collection failed.
  pause
  exit /b %ERRORLEVEL%
)

echo [done] Evidence pack created under:
echo        %BASE_DIR%smoke_evidence\artifacts

echo Opening artifact folder...
start "" "%BASE_DIR%smoke_evidence\artifacts"

exit /b 0
