@echo off
setlocal

set "BASE_DIR=%~dp0"
set "APP_EXE=%BASE_DIR%AIUsageWatcher.exe"
set "COLLECTOR_FLAT=%BASE_DIR%agent\src\collector.py"
set "COLLECTOR_INTERNAL=%BASE_DIR%_internal\agent\src\collector.py"
set "ENV_FILE=%BASE_DIR%.env"
set "ENV_EXAMPLE=%BASE_DIR%.env.example"

if not exist "%APP_EXE%" (
  echo [ERROR] AIUsageWatcher.exe not found in:
  echo         %BASE_DIR%
  echo.
  echo Build the onedir bundle first or copy this launcher into the bundle folder.
  pause
  exit /b 1
)

set "BUNDLE_LAYOUT="
if exist "%COLLECTOR_FLAT%" set "BUNDLE_LAYOUT=flat"
if not defined BUNDLE_LAYOUT if exist "%COLLECTOR_INTERNAL%" set "BUNDLE_LAYOUT=_internal"
if not defined BUNDLE_LAYOUT (
  echo [ERROR] agent runtime path not found.
  echo         Expected either:
  echo         %COLLECTOR_FLAT%
  echo         %COLLECTOR_INTERNAL%
  echo.
  echo Rebuild the onedir bundle before launching.
  pause
  exit /b 1
)
echo [INFO] Bundle layout detected: %BUNDLE_LAYOUT%

if not exist "%ENV_FILE%" (
  if exist "%ENV_EXAMPLE%" (
    copy /Y "%ENV_EXAMPLE%" "%ENV_FILE%" >nul
    echo [INFO] Created .env from .env.example.
    echo [INFO] Fill OAuth variables in .env before login.
  ) else (
    echo [WARN] .env and .env.example are both missing.
  )
)

"%APP_EXE%"
set "EXIT_CODE=%ERRORLEVEL%"
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] AIUsageWatcher exited with code %EXIT_CODE%.
  pause
)

exit /b %EXIT_CODE%
