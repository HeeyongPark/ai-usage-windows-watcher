param(
    [string]$OutputPath = "",
    [string]$BundleRoot = "",
    [string]$RunId = ""
)

function Resolve-WorkspacePath {
    param(
        [string]$PathValue,
        [string]$BasePath
    )

    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return [System.IO.Path]::GetFullPath($PathValue)
    }

    return [System.IO.Path]::GetFullPath((Join-Path $BasePath $PathValue))
}

function Resolve-DesktopRoot {
    param(
        [string]$ScriptRoot
    )

    $resolvedScriptRoot = [System.IO.Path]::GetFullPath($ScriptRoot)
    $scriptParent = [System.IO.Path]::GetFullPath((Join-Path $resolvedScriptRoot ".."))

    if (Test-Path (Join-Path $scriptParent "src\\app.py")) {
        return $scriptParent
    }

    if (Test-Path (Join-Path $resolvedScriptRoot "AIUsageWatcher.exe")) {
        return $resolvedScriptRoot
    }

    if (Test-Path (Join-Path $scriptParent "AIUsageWatcher.exe")) {
        return $scriptParent
    }

    return $scriptParent
}

$desktopRoot = Resolve-DesktopRoot -ScriptRoot $PSScriptRoot
$bundleMode = (Test-Path (Join-Path $desktopRoot "AIUsageWatcher.exe"))
if (-not $RunId) {
    $RunId = (Get-Date).ToString("yyyyMMdd-HHmmss")
}

if (-not $OutputPath) {
    if ($bundleMode) {
        $OutputPath = ("smoke_evidence\\artifacts\\runtime-context-{0}.json" -f $RunId)
    } else {
        $OutputPath = "tests\\manual\\artifacts\\runtime-context.json"
    }
}

if (-not $BundleRoot) {
    if ($bundleMode) {
        $BundleRoot = "."
    } else {
        $BundleRoot = "dist\\AIUsageWatcher"
    }
}

$resolvedOutputPath = Resolve-WorkspacePath -PathValue $OutputPath -BasePath $desktopRoot
$resolvedBundleRoot = Resolve-WorkspacePath -PathValue $BundleRoot -BasePath $desktopRoot

$pythonVersion = "unknown"
try {
    $pythonVersion = (python --version 2>&1 | Out-String).Trim()
} catch {
    $pythonVersion = "python not found"
}

$resolutionList = @()
try {
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
    foreach ($screen in [System.Windows.Forms.Screen]::AllScreens) {
        $resolutionList += @{
            name = $screen.DeviceName
            width = $screen.Bounds.Width
            height = $screen.Bounds.Height
            primary = $screen.Primary
        }
    }
} catch {
    $resolutionList += @{
        name = "unavailable"
        width = 0
        height = 0
        primary = $false
    }
}

$bundleExePath = Join-Path $resolvedBundleRoot "AIUsageWatcher.exe"
$launcherPath = Join-Path $resolvedBundleRoot "run_ai_usage_watcher.bat"
$collectorFlatPath = Join-Path $resolvedBundleRoot "agent\\src\\collector.py"
$collectorInternalPath = Join-Path $resolvedBundleRoot "_internal\\agent\\src\\collector.py"

$bundleLayout = "missing"
if (Test-Path $collectorInternalPath) {
    $bundleLayout = "_internal"
} elseif (Test-Path $collectorFlatPath) {
    $bundleLayout = "flat"
}

$bundleExeHash = ""
if (Test-Path $bundleExePath) {
    try {
        $bundleExeHash = (Get-FileHash -Path $bundleExePath -Algorithm SHA256).Hash
    } catch {
        $bundleExeHash = "hash_error"
    }
}

$osInfo = Get-CimInstance Win32_OperatingSystem
$defaultDbPath = Join-Path $env:USERPROFILE ".ai-usage-watcher\\usage.db"
$runtimeContext = [ordered]@{
    run_id = $RunId
    captured_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
    computer_name = $env:COMPUTERNAME
    user_name = $env:USERNAME
    os_caption = $osInfo.Caption
    os_version = $osInfo.Version
    python_version = $pythonVersion
    appdata = $env:APPDATA
    db_path = if ($env:AUIW_DB_PATH) { $env:AUIW_DB_PATH } else { $defaultDbPath }
    oauth_token_path = Join-Path $env:APPDATA "AIUsageWatcher\\oauth_token.json"
    bundle_root = $resolvedBundleRoot
    bundle_layout = $bundleLayout
    bundle_exe_path = $bundleExePath
    bundle_exe_exists = (Test-Path $bundleExePath)
    bundle_exe_sha256 = $bundleExeHash
    launcher_path = $launcherPath
    launcher_exists = (Test-Path $launcherPath)
    collector_flat_path = $collectorFlatPath
    collector_flat_exists = (Test-Path $collectorFlatPath)
    collector_internal_path = $collectorInternalPath
    collector_internal_exists = (Test-Path $collectorInternalPath)
    screens = $resolutionList
}

$outputDir = Split-Path -Parent $resolvedOutputPath
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$json = $runtimeContext | ConvertTo-Json -Depth 5
Set-Content -Path $resolvedOutputPath -Value $json -Encoding UTF8

Write-Host "Saved runtime context: $resolvedOutputPath"
