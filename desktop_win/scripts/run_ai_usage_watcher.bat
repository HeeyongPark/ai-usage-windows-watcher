@echo off
setlocal

set "BASE_DIR=%~dp0"
set "APP_EXE=%BASE_DIR%AIUsageWatcher.exe"
set "COLLECTOR_FLAT=%BASE_DIR%agent\src\collector.py"
set "COLLECTOR_INTERNAL=%BASE_DIR%_internal\agent\src\collector.py"
set "PY_ABI_DLL_INTERNAL=%BASE_DIR%_internal\python3.dll"
set "PY_ABI_DLL_FLAT=%BASE_DIR%python3.dll"
set "VC_RUNTIME_INTERNAL=%BASE_DIR%_internal\vcruntime140.dll"
set "VC_RUNTIME_FLAT=%BASE_DIR%vcruntime140.dll"
set "VC_RUNTIME_1_INTERNAL=%BASE_DIR%_internal\vcruntime140_1.dll"
set "VC_RUNTIME_1_FLAT=%BASE_DIR%vcruntime140_1.dll"
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

echo %BASE_DIR% | find /I "\build\dist\" >nul
if %ERRORLEVEL%==0 (
  echo [WARN] Running from a non-standard bundle path:
  echo        %BASE_DIR%
  echo [WARN] Use desktop_win\dist\AIUsageWatcher\run_ai_usage_watcher.bat from the latest build output.
)

echo %BASE_DIR% | find /I "OneDrive" >nul
if %ERRORLEVEL%==0 (
  echo [WARN] Bundle is inside OneDrive. If runtime DLL errors occur, set this folder to "Always keep on this device".
)

set "PY_RUNTIME_DLL="
for %%F in ("%BASE_DIR%_internal\python3?.dll" "%BASE_DIR%_internal\python3??.dll" "%BASE_DIR%_internal\python3???.dll" "%BASE_DIR%python3?.dll" "%BASE_DIR%python3??.dll" "%BASE_DIR%python3???.dll") do (
  if exist "%%~fF" (
    if /I not "%%~nxF"=="python3.dll" (
      if not defined PY_RUNTIME_DLL set "PY_RUNTIME_DLL=%%~fF"
    )
  )
)
if not defined PY_RUNTIME_DLL (
  echo [ERROR] Python runtime DLL (python3XX.dll) is missing from the bundle.
  echo [ERROR] Rebuild via desktop_win\scripts\build_windows_bundle.ps1 and rerun from dist\AIUsageWatcher.
  pause
  exit /b 1
)
echo [INFO] Python runtime DLL detected: %PY_RUNTIME_DLL%

set "PY_ABI_DLL="
if exist "%PY_ABI_DLL_INTERNAL%" set "PY_ABI_DLL=%PY_ABI_DLL_INTERNAL%"
if not defined PY_ABI_DLL if exist "%PY_ABI_DLL_FLAT%" set "PY_ABI_DLL=%PY_ABI_DLL_FLAT%"
if not defined PY_ABI_DLL (
  echo [ERROR] python3.dll is missing from the bundle.
  echo [ERROR] Rebuild the bundle. This file is required by python3XX.dll.
  pause
  exit /b 1
)

set "VC_RUNTIME="
if exist "%VC_RUNTIME_INTERNAL%" set "VC_RUNTIME=%VC_RUNTIME_INTERNAL%"
if not defined VC_RUNTIME if exist "%VC_RUNTIME_FLAT%" set "VC_RUNTIME=%VC_RUNTIME_FLAT%"
if not defined VC_RUNTIME (
  echo [WARN] vcruntime140.dll not found in bundle. Install Microsoft Visual C++ Redistributable if launch fails.
)

set "VC_RUNTIME_1="
if exist "%VC_RUNTIME_1_INTERNAL%" set "VC_RUNTIME_1=%VC_RUNTIME_1_INTERNAL%"
if not defined VC_RUNTIME_1 if exist "%VC_RUNTIME_1_FLAT%" set "VC_RUNTIME_1=%VC_RUNTIME_1_FLAT%"
if not defined VC_RUNTIME_1 (
  echo [WARN] vcruntime140_1.dll not found in bundle. Install Microsoft Visual C++ Redistributable if launch fails.
)

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
