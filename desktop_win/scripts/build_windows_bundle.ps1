param(
    [string]$PythonExe = "python",
    [string]$ProjectRoot = ""
)

$ErrorActionPreference = "Stop"

if ($env:OS -ne "Windows_NT") {
    throw "This script must run on Windows."
}

if (-not $ProjectRoot) {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
} else {
    $ProjectRoot = (Resolve-Path $ProjectRoot).Path
}

$DesktopRoot = Join-Path $ProjectRoot "desktop_win"
$AgentRoot = Join-Path $ProjectRoot "agent"
$BuildVenv = Join-Path $DesktopRoot ".build-venv"
$BuildPython = Join-Path $BuildVenv "Scripts\python.exe"
$BuildPyInstaller = Join-Path $BuildVenv "Scripts\pyinstaller.exe"

$AppName = "AIUsageWatcher"
$DistRoot = Join-Path $DesktopRoot "dist"
$BundleRoot = Join-Path $DistRoot $AppName
$BuildWorkDir = Join-Path $DesktopRoot "build"
$SpecPath = Join-Path $DesktopRoot "$AppName.spec"

function Ensure-RuntimeDllSet {
    param(
        [string]$BundleRootPath,
        [string]$BuildPythonPath
    )

    $bundleInternalDir = Join-Path -Path ([string]$BundleRootPath) -ChildPath "_internal"
    $buildPythonDir = Split-Path -Parent $BuildPythonPath
    $buildVenvRoot = Split-Path -Parent $buildPythonDir
    $runtimeInfoJson = (& $BuildPythonPath -c "import json, os, sys; print(json.dumps({'abi': f'python{sys.version_info.major}{sys.version_info.minor}.dll', 'base_prefix': sys.base_prefix, 'base_dlls': os.path.join(sys.base_prefix, 'DLLs')}))" | Out-String).Trim()
    if (-not $runtimeInfoJson) {
        throw "Unable to resolve runtime metadata from build interpreter."
    }

    $runtimeInfo = $runtimeInfoJson | ConvertFrom-Json
    $pythonDllName = [string]$runtimeInfo.abi
    if (-not $pythonDllName) {
        throw "Unable to resolve Python DLL name from build interpreter."
    }

    $sourceSearchDirs = @()
    foreach ($candidateDir in @(
        $buildPythonDir,
        $buildVenvRoot,
        [string]$runtimeInfo.base_prefix,
        [string]$runtimeInfo.base_dlls
    )) {
        if (-not $candidateDir) {
            continue
        }

        $candidateDir = [string]$candidateDir
        if (-not (Test-Path -Path $candidateDir)) {
            continue
        }

        if ($sourceSearchDirs -notcontains $candidateDir) {
            $sourceSearchDirs += $candidateDir
        }
    }

    $runtimeDllRules = @(
        @{ Name = $pythonDllName; Required = $true },
        @{ Name = "python3.dll"; Required = $true },
        @{ Name = "vcruntime140.dll"; Required = $false },
        @{ Name = "vcruntime140_1.dll"; Required = $false }
    )

    foreach ($rule in $runtimeDllRules) {
        $dllName = [string]$rule["Name"]
        $dllRequired = [bool]$rule["Required"]

        $bundleCandidates = @(
            Join-Path -Path ([string]$bundleInternalDir) -ChildPath $dllName,
            Join-Path -Path ([string]$BundleRootPath) -ChildPath $dllName
        )
        $bundleHit = $bundleCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
        if ($bundleHit) {
            Write-Host "[check] runtime DLL present: $dllName"
            continue
        }

        $sourceCandidate = $null
        foreach ($sourceDir in $sourceSearchDirs) {
            $candidate = Join-Path -Path ([string]$sourceDir) -ChildPath $dllName
            if (Test-Path $candidate) {
                $sourceCandidate = $candidate
                break
            }
        }

        if ($sourceCandidate) {
            if (-not (Test-Path $bundleInternalDir)) {
                New-Item -ItemType Directory -Path $bundleInternalDir -Force | Out-Null
            }
            $targetPath = Join-Path -Path ([string]$bundleInternalDir) -ChildPath $dllName
            Copy-Item -Path $sourceCandidate -Destination $targetPath -Force
            Write-Host "[fixup] copied runtime DLL: $dllName"
            continue
        }

        if ($dllRequired) {
            $searched = ($sourceSearchDirs -join ", ")
            throw "Required runtime DLL missing from bundle and known source dirs: $dllName (searched: $searched)"
        }

        $searched = ($sourceSearchDirs -join ", ")
        Write-Warning "Optional runtime DLL missing: $dllName (searched: $searched)"
    }
}

if (-not (Test-Path $BuildPython)) {
    Write-Host "[build] Creating build virtualenv at $BuildVenv"
    & $PythonExe -m venv $BuildVenv
}

Write-Host "[build] Installing build dependencies"
& $BuildPython -m pip install --upgrade pip
& $BuildPython -m pip install pyinstaller==6.11.1
& $BuildPython -m pip install -r (Join-Path $AgentRoot "requirements.txt")

Write-Host "[build] Cleaning old artifacts"
if (Test-Path $BuildWorkDir) {
    Remove-Item -Path $BuildWorkDir -Recurse -Force
}
if (Test-Path $DistRoot) {
    Remove-Item -Path $DistRoot -Recurse -Force
}
if (Test-Path $SpecPath) {
    Remove-Item -Path $SpecPath -Force
}

Write-Host "[build] Running PyInstaller (onedir)"
Push-Location $DesktopRoot
try {
    & $BuildPyInstaller `
        --noconfirm `
        --clean `
        --onedir `
        --contents-directory "_internal" `
        --windowed `
        --name $AppName `
        --distpath $DistRoot `
        --workpath $BuildWorkDir `
        --specpath $DesktopRoot `
        --add-data "$AgentRoot\src;agent/src" `
        --add-data "$AgentRoot\sql;agent/sql" `
        --add-data "$DesktopRoot\.env.example;." `
        ".\src\app.py"
}
finally {
    Pop-Location
}

if (-not (Test-Path $BundleRoot)) {
    throw "Bundle output not found: $BundleRoot"
}

$CollectorFlat = Join-Path $BundleRoot "agent\src\collector.py"
$CollectorInternal = Join-Path $BundleRoot "_internal\agent\src\collector.py"
if (-not (Test-Path $CollectorFlat) -and -not (Test-Path $CollectorInternal)) {
    throw "Bundle agent path missing: collector.py was not found under flat or _internal layout."
}

Ensure-RuntimeDllSet -BundleRootPath $BundleRoot -BuildPythonPath $BuildPython

$LauncherSource = Join-Path $DesktopRoot "scripts\run_ai_usage_watcher.bat"
$LauncherTarget = Join-Path $BundleRoot "run_ai_usage_watcher.bat"
Copy-Item -Path $LauncherSource -Destination $LauncherTarget -Force

$PrepareEvidenceSource = Join-Path $DesktopRoot "scripts\prepare_windows_smoke_evidence.ps1"
$PrepareEvidenceTarget = Join-Path $BundleRoot "prepare_windows_smoke_evidence.ps1"
Copy-Item -Path $PrepareEvidenceSource -Destination $PrepareEvidenceTarget -Force

$ProbeSource = Join-Path $DesktopRoot "scripts\windows_runtime_probe.ps1"
$ProbeTarget = Join-Path $BundleRoot "windows_runtime_probe.ps1"
Copy-Item -Path $ProbeSource -Destination $ProbeTarget -Force

$CollectEvidenceSource = Join-Path $DesktopRoot "scripts\collect_windows_smoke_evidence.bat"
$CollectEvidenceTarget = Join-Path $BundleRoot "collect_windows_smoke_evidence.bat"
Copy-Item -Path $CollectEvidenceSource -Destination $CollectEvidenceTarget -Force

$SmokeEvidenceTemplateDir = Join-Path $BundleRoot "smoke_evidence\templates"
if (-not (Test-Path $SmokeEvidenceTemplateDir)) {
    New-Item -ItemType Directory -Path $SmokeEvidenceTemplateDir -Force | Out-Null
}
Copy-Item `
    -Path (Join-Path $DesktopRoot "tests\manual\windows-runtime-smoke-checklist.md") `
    -Destination (Join-Path $SmokeEvidenceTemplateDir "windows-runtime-smoke-checklist.md") `
    -Force
Copy-Item `
    -Path (Join-Path $DesktopRoot "tests\manual\windows-runtime-evidence-template.md") `
    -Destination (Join-Path $SmokeEvidenceTemplateDir "windows-runtime-evidence-template.md") `
    -Force

$EnvExampleSource = Join-Path $DesktopRoot ".env.example"
$EnvExampleTarget = Join-Path $BundleRoot ".env.example"
Copy-Item -Path $EnvExampleSource -Destination $EnvExampleTarget -Force

$EnvTarget = Join-Path $BundleRoot ".env"
if (-not (Test-Path $EnvTarget)) {
    Copy-Item -Path $EnvExampleSource -Destination $EnvTarget
}

$BundleLayout = "flat"
if (Test-Path $CollectorInternal) {
    $BundleLayout = "_internal"
}

Write-Host ""
Write-Host "[done] onedir bundle created:"
Write-Host "       $BundleRoot"
Write-Host "[info] bundle layout: $BundleLayout"
Write-Host "[next] edit .env and run run_ai_usage_watcher.bat"
