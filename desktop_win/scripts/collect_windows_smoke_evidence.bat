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

rem %~dp0 ends with a backslash (e.g. C:\...\AIUsageWatcher\).
rem Passing it inside "..." to PowerShell causes cmd.exe to escape the closing "
rem as \" making the path arrive as  C:\...\AIUsageWatcher"  (with a trailing quote).
rem Fix: strip the trailing backslash before embedding in the PowerShell call.
set "BUNDLE_ROOT=%BASE_DIR:~0,-1%"

if defined RUN_ID (
  powershell -ExecutionPolicy Bypass -File "%PREPARE_SCRIPT%" -BundleRoot "%BUNDLE_ROOT%" -RunId "%RUN_ID%"
) else (
  powershell -ExecutionPolicy Bypass -File "%PREPARE_SCRIPT%" -BundleRoot "%BUNDLE_ROOT%"
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
