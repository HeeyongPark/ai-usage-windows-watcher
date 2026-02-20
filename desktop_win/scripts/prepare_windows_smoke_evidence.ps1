param(
    [string]$RunId = "",
    [string]$OutputDir = "",
    [string]$BundleRoot = "",
    [string]$ChecklistTemplatePath = "",
    [string]$EvidenceTemplatePath = ""
)

$ErrorActionPreference = "Stop"

function Normalize-PathInput {
    param(
        [string]$PathValue
    )

    if ($null -eq $PathValue) {
        return ""
    }

    $normalized = $PathValue.Trim()
    if ($normalized.Length -ge 2) {
        $startsWithDouble = $normalized.StartsWith('"')
        $endsWithDouble = $normalized.EndsWith('"')
        $startsWithSingle = $normalized.StartsWith("'")
        $endsWithSingle = $normalized.EndsWith("'")
        if (($startsWithDouble -and $endsWithDouble) -or ($startsWithSingle -and $endsWithSingle)) {
            $normalized = $normalized.Substring(1, $normalized.Length - 2).Trim()
        }
    }

    # Strip common control characters that can leak from shell wrappers.
    $normalized = $normalized -replace "[\u0000-\u001F]", ""
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

function Resolve-TemplatePath {
    param(
        [string]$ExplicitPath,
        [string[]]$RelativeCandidates,
        [string]$BasePath,
        [string]$Label
    )

    if ($ExplicitPath) {
        $resolvedExplicit = Resolve-WorkspacePath -PathValue $ExplicitPath -BasePath $BasePath
        if (Test-Path $resolvedExplicit) {
            return $resolvedExplicit
        }
        throw "$Label template not found: $resolvedExplicit"
    }

    foreach ($candidate in $RelativeCandidates) {
        $resolvedCandidate = Resolve-WorkspacePath -PathValue $candidate -BasePath $BasePath
        if (Test-Path $resolvedCandidate) {
            return $resolvedCandidate
        }
    }

    throw "$Label template not found under supported locations."
}

$desktopRoot = Resolve-DesktopRoot -ScriptRoot $PSScriptRoot
$bundleMode = (Test-Path (Join-Path $desktopRoot "AIUsageWatcher.exe"))
if (-not $RunId) {
    $RunId = (Get-Date).ToString("yyyyMMdd-HHmmss")
}

if (-not $BundleRoot) {
    if ($bundleMode) {
        $BundleRoot = "."
    } else {
        $BundleRoot = "dist\\AIUsageWatcher"
    }
}

if (-not $OutputDir) {
    if ($bundleMode) {
        $OutputDir = "smoke_evidence\\artifacts"
    } else {
        $OutputDir = "tests\\manual\\artifacts"
    }
}

$resolvedOutputDir = Resolve-WorkspacePath -PathValue $OutputDir -BasePath $desktopRoot
if (-not (Test-Path $resolvedOutputDir)) {
    New-Item -ItemType Directory -Path $resolvedOutputDir -Force | Out-Null
}

$runtimeContextPath = Join-Path $resolvedOutputDir ("runtime-context-{0}.json" -f $RunId)
$checklistSource = Resolve-TemplatePath `
    -ExplicitPath $ChecklistTemplatePath `
    -RelativeCandidates @(
        "tests\\manual\\windows-runtime-smoke-checklist.md",
        "smoke_evidence\\templates\\windows-runtime-smoke-checklist.md"
    ) `
    -BasePath $desktopRoot `
    -Label "Checklist"
$checklistTarget = Join-Path $resolvedOutputDir ("windows-runtime-smoke-checklist-{0}.md" -f $RunId)
$evidenceTemplate = Resolve-TemplatePath `
    -ExplicitPath $EvidenceTemplatePath `
    -RelativeCandidates @(
        "tests\\manual\\windows-runtime-evidence-template.md",
        "smoke_evidence\\templates\\windows-runtime-evidence-template.md"
    ) `
    -BasePath $desktopRoot `
    -Label "Evidence"
$evidenceTarget = Join-Path $resolvedOutputDir ("windows-runtime-evidence-{0}.md" -f $RunId)

Copy-Item -Path $checklistSource -Destination $checklistTarget -Force

$probeCandidates = @(
    (Join-Path $PSScriptRoot "windows_runtime_probe.ps1"),
    (Join-Path $desktopRoot "scripts\\windows_runtime_probe.ps1")
)
$probeScript = ""
foreach ($candidate in $probeCandidates) {
    if ($candidate -and (Test-Path $candidate)) {
        $probeScript = $candidate
        break
    }
}
if (-not $probeScript) {
    throw "windows_runtime_probe.ps1 not found near script root or desktop scripts directory."
}

& $probeScript -OutputPath $runtimeContextPath -BundleRoot $BundleRoot -RunId $RunId

if (-not (Test-Path $runtimeContextPath)) {
    throw "Runtime context was not generated: $runtimeContextPath"
}

$runtimeContext = Get-Content -Path $runtimeContextPath -Raw | ConvertFrom-Json
$osLabel = "$($runtimeContext.os_caption) ($($runtimeContext.os_version))"
$timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ssK")
$checklistDisplay = ($checklistTarget -replace "\\", "/")
$runtimeContextDisplay = ($runtimeContextPath -replace "\\", "/")

$evidenceText = Get-Content -Path $evidenceTemplate -Raw
$evidenceText = $evidenceText -replace "(?m)^- Run id:.*$", "- Run id: $RunId"
$evidenceText = $evidenceText -replace "(?m)^- Date/time:.*$", "- Date/time: $timestamp"
$evidenceText = $evidenceText -replace "(?m)^- Machine:.*$", "- Machine: $($runtimeContext.computer_name)"
$evidenceText = $evidenceText -replace "(?m)^- OS:.*$", "- OS: $osLabel"
$evidenceText = $evidenceText -replace "(?m)^- Bundle path:.*$", "- Bundle path: $($runtimeContext.bundle_root)"
$evidenceText = $evidenceText -replace "(?m)^- Bundle layout:.*$", "- Bundle layout: $($runtimeContext.bundle_layout)"
$evidenceText = $evidenceText -replace "(?m)^- Launcher path:.*$", "- Launcher path: $($runtimeContext.launcher_path)"
$evidenceText = $evidenceText -replace "runtime-context-<run-id>\\.json", ("runtime-context-{0}.json" -f $RunId)
$evidenceText = [regex]::Replace(
    $evidenceText,
    '(?m)^  - `.*runtime-context-.*`$',
    ('  - `{0}`' -f $runtimeContextDisplay)
)
$evidenceText = [regex]::Replace(
    $evidenceText,
    '(?m)^  - `.*windows-runtime-smoke-checklist.*`$',
    ('  - `{0}`' -f $checklistDisplay)
)
$evidenceText = $evidenceText -replace "(?m)^- Bundle checksum \(optional\):.*$", "- Bundle checksum (optional): $($runtimeContext.bundle_exe_sha256)"

Set-Content -Path $evidenceTarget -Value $evidenceText -Encoding UTF8

Write-Host "[done] Windows smoke evidence pack created."
Write-Host "       Run ID: $RunId"
Write-Host "       Runtime context: $runtimeContextPath"
Write-Host "       Checklist copy: $checklistTarget"
Write-Host "       Evidence file: $evidenceTarget"
