param(
    [string]$OutputPath = "tests\\manual\\artifacts\\runtime-context.json"
)

$desktopRoot = Split-Path -Parent $PSScriptRoot
if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $resolvedOutputPath = $OutputPath
} else {
    $resolvedOutputPath = Join-Path $desktopRoot $OutputPath
}

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

$defaultDbPath = Join-Path $env:USERPROFILE ".ai-usage-watcher\\usage.db"
$runtimeContext = [ordered]@{
    captured_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")
    computer_name = $env:COMPUTERNAME
    user_name = $env:USERNAME
    os_caption = (Get-CimInstance Win32_OperatingSystem).Caption
    os_version = (Get-CimInstance Win32_OperatingSystem).Version
    python_version = $pythonVersion
    appdata = $env:APPDATA
    db_path = if ($env:AUIW_DB_PATH) { $env:AUIW_DB_PATH } else { $defaultDbPath }
    oauth_token_path = Join-Path $env:APPDATA "AIUsageWatcher\\oauth_token.json"
    screens = $resolutionList
}

$outputDir = Split-Path -Parent $resolvedOutputPath
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$json = $runtimeContext | ConvertTo-Json -Depth 5
Set-Content -Path $resolvedOutputPath -Value $json -Encoding UTF8

Write-Host "Saved runtime context: $resolvedOutputPath"
