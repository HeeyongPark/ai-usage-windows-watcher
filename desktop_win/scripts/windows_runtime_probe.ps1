param(
    [string]$OutputPath = "",
    [string]$BundleRoot = "",
    [string]$RunId = ""
)

function Normalize-PathInput {
    param(
        [string]$PathValue
    )

    if ($null -eq $PathValue) {
        return ""
    }

    $normalized = $PathValue.Trim()

    # Strip common control characters that can leak from shell wrappers.
    $normalized = $normalized -replace "[\u0000-\u001F]", ""

    if ($normalized.Length -ge 2) {
        $startsWithDouble = $normalized.StartsWith('"')
        $endsWithDouble   = $normalized.EndsWith('"')
        $startsWithSingle = $normalized.StartsWith("'")
        $endsWithSingle   = $normalized.EndsWith("'")

        # Case 1: symmetric quotes -> remove both
        if (($startsWithDouble -and $endsWithDouble) -or ($startsWithSingle -and $endsWithSingle)) {
            $normalized = $normalized.Substring(1, $normalized.Length - 2).Trim()
        }
        # Case 2: trailing orphan quote only (cmd.exe set "VAR=path\" bug)
        #   e.g. C:\path\to\dir" -> C:\path\to\dir
        elseif ($endsWithDouble -and -not $startsWithDouble) {
            $normalized = $normalized.TrimEnd('"').Trim()
        }
        elseif ($endsWithSingle -and -not $startsWithSingle) {
            $normalized = $normalized.TrimEnd("'").Trim()
        }
        # Case 3: leading orphan quote only
        elseif ($startsWithDouble -and -not $endsWithDouble) {
            $normalized = $normalized.TrimStart('"').Trim()
        }
        elseif ($startsWithSingle -and -not $endsWithSingle) {
            $normalized = $normalized.TrimStart("'").Trim()
        }
    }

    return $normalized
}

function Resolve-WorkspacePath {
    param(
        [string]$PathValue,
        [string]$BasePath
    )

    $safePathValue = Normalize-PathInput -PathValue $PathValue
    $safeBasePath = Normalize-PathInput -PathValue $BasePath

    if (-not $safePathValue) {
        throw "Path input is empty after normalization."
    }

    $isRooted = $false
    try {
        $isRooted = [System.IO.Path]::IsPathRooted($safePathValue)
    } catch {
        throw "Invalid path input: '$safePathValue' ($($_.Exception.Message))"
    }

    try {
        if ($isRooted) {
            return [System.IO.Path]::GetFullPath($safePathValue)
        }
        return [System.IO.Path]::GetFullPath((Join-Path $safeBasePath $safePathValue))
    } catch {
        throw "Failed to resolve path. value='$safePathValue', base='$safeBasePath' ($($_.Exception.Message))"
    }
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
$pythonAbiInternalPath = Join-Path $resolvedBundleRoot "_internal\\python3.dll"
$pythonAbiFlatPath = Join-Path $resolvedBundleRoot "python3.dll"
$vcRuntimeInternalPath = Join-Path $resolvedBundleRoot "_internal\\vcruntime140.dll"
$vcRuntimeFlatPath = Join-Path $resolvedBundleRoot "vcruntime140.dll"
$vcRuntime1InternalPath = Join-Path $resolvedBundleRoot "_internal\\vcruntime140_1.dll"
$vcRuntime1FlatPath = Join-Path $resolvedBundleRoot "vcruntime140_1.dll"
$sqliteExtInternalPath = Join-Path $resolvedBundleRoot "_internal\\_sqlite3.pyd"
$sqliteExtFlatPath = Join-Path $resolvedBundleRoot "_sqlite3.pyd"

$pythonRuntimeDllPath = ""
$pythonRuntimeCandidates = @()
if (Test-Path (Join-Path $resolvedBundleRoot "_internal")) {
    $pythonRuntimeCandidates += Get-ChildItem -Path (Join-Path $resolvedBundleRoot "_internal") -Filter "python3*.dll" -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "python3.dll" }
}
if (Test-Path $resolvedBundleRoot) {
    $pythonRuntimeCandidates += Get-ChildItem -Path $resolvedBundleRoot -Filter "python3*.dll" -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne "python3.dll" }
}
if ($pythonRuntimeCandidates.Count -gt 0) {
    $pythonRuntimeDllPath = $pythonRuntimeCandidates[0].FullName
}

$pythonAbiPath = ""
if (Test-Path $pythonAbiInternalPath) {
    $pythonAbiPath = $pythonAbiInternalPath
} elseif (Test-Path $pythonAbiFlatPath) {
    $pythonAbiPath = $pythonAbiFlatPath
}

$vcRuntimePath = ""
if (Test-Path $vcRuntimeInternalPath) {
    $vcRuntimePath = $vcRuntimeInternalPath
} elseif (Test-Path $vcRuntimeFlatPath) {
    $vcRuntimePath = $vcRuntimeFlatPath
}

$vcRuntime1Path = ""
if (Test-Path $vcRuntime1InternalPath) {
    $vcRuntime1Path = $vcRuntime1InternalPath
} elseif (Test-Path $vcRuntime1FlatPath) {
    $vcRuntime1Path = $vcRuntime1FlatPath
}

$sqliteExtPath = ""
if (Test-Path $sqliteExtInternalPath) {
    $sqliteExtPath = $sqliteExtInternalPath
} elseif (Test-Path $sqliteExtFlatPath) {
    $sqliteExtPath = $sqliteExtFlatPath
}

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
    python_runtime_dll_path = $pythonRuntimeDllPath
    python_runtime_dll_exists = [bool]$pythonRuntimeDllPath
    python_abi_dll_path = $pythonAbiPath
    python_abi_dll_exists = [bool]$pythonAbiPath
    vcruntime140_dll_path = $vcRuntimePath
    vcruntime140_dll_exists = [bool]$vcRuntimePath
    vcruntime140_1_dll_path = $vcRuntime1Path
    vcruntime140_1_dll_exists = [bool]$vcRuntime1Path
    sqlite_ext_path = $sqliteExtPath
    sqlite_ext_exists = [bool]$sqliteExtPath
    screens = $resolutionList
}

$outputDir = Split-Path -Parent $resolvedOutputPath
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$json = $runtimeContext | ConvertTo-Json -Depth 5
Set-Content -Path $resolvedOutputPath -Value $json -Encoding UTF8

Write-Host "Saved runtime context: $resolvedOutputPath"
