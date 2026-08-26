[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$MinimumFreeBytes = 10GB
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Get-RequiredApplication {
    param([Parameter(Mandatory = $true)][string]$Name)

    $command = Get-Command $Name -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if (-not $command) {
        throw "Required program '$Name' was not found. Stop here and follow the Phase 0 PC runbook."
    }
    return $command.Source
}

function Invoke-LoggedCommand {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [Parameter(Mandatory = $true)][string]$WorkingDirectory,
        [Parameter(Mandatory = $true)][string]$LogPath
    )

    Push-Location $WorkingDirectory
    try {
        $rawOutput = @(& $FilePath @Arguments 2>&1)
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    $output = @($rawOutput | ForEach-Object { $_.ToString() })
    [System.IO.File]::WriteAllText(
        $LogPath,
        (($output -join [Environment]::NewLine) + [Environment]::NewLine),
        $Utf8NoBom
    )
    if ($exitCode -ne 0) {
        throw "Command failed with exit code $exitCode. Review the local log: $LogPath"
    }
    return $output
}

function Save-ProcessEnvironment {
    param([Parameter(Mandatory = $true)][string[]]$Names)

    $saved = @{}
    foreach ($name in $Names) {
        $saved[$name] = [Environment]::GetEnvironmentVariable($name, "Process")
    }
    return $saved
}

function Restore-ProcessEnvironment {
    param([Parameter(Mandatory = $true)][hashtable]$Saved)

    foreach ($entry in $Saved.GetEnumerator()) {
        [Environment]::SetEnvironmentVariable($entry.Key, $entry.Value, "Process")
    }
}

function Write-JsonNoBom {
    param(
        [Parameter(Mandatory = $true)]$Value,
        [Parameter(Mandatory = $true)][string]$Path
    )

    $json = $Value | ConvertTo-Json -Depth 10
    [System.IO.File]::WriteAllText(
        $Path,
        ($json + [Environment]::NewLine),
        $Utf8NoBom
    )
}

if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw "This controlled evaluation harness is for Windows only."
}

$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($identity)
if ($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "Run this in a normal, non-administrator PowerShell window."
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$PinPath = Join-Path $RepoRoot "foundation/openjarvis/PIN.json"
$AssessorPath = Join-Path $RepoRoot "scripts/assess_openjarvis_source.py"
$OutputRoot = Join-Path $RepoRoot "artifacts/phase0/openjarvis-evaluation"
$RunId = (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssfffZ")
$RunRoot = Join-Path $OutputRoot (Join-Path "runs" $RunId)

$driveRoot = [System.IO.Path]::GetPathRoot($OutputRoot)
$driveName = $driveRoot.Substring(0, 1)
$drive = Get-PSDrive -Name $driveName
if ($drive.Free -lt $MinimumFreeBytes) {
    throw "At least 10 GiB of free disk space is required for this evaluation."
}

$Git = Get-RequiredApplication "git"
$Python = Get-RequiredApplication "python"
$Uv = Get-RequiredApplication "uv"

$pythonVersionText = (& $Python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))" |
    Select-Object -First 1).ToString().Trim()
if ($LASTEXITCODE -ne 0) {
    throw "Python could not report its version."
}
$pythonVersion = [Version]$pythonVersionText
if ($pythonVersion.Major -ne 3 -or $pythonVersion.Minor -lt 10 -or $pythonVersion.Minor -gt 13) {
    throw "Python 3.10 through 3.13 is required. Found $pythonVersionText."
}

$pin = Get-Content -Path $PinPath -Raw | ConvertFrom-Json
if ($null -ne $pin.selected) {
    throw "The candidate pin unexpectedly contains a selection; Phase 0 comparison must remain open."
}
if ([int]$pin.patch_count -ne 0) {
    throw "The candidate pin unexpectedly records upstream patches."
}
if ([string]$pin.upstream -ne "https://github.com/open-jarvis/OpenJarvis") {
    throw "The pinned upstream repository is not the approved OpenJarvis source."
}

New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $OutputRoot "candidates") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $OutputRoot "uv-cache") -Force | Out-Null

$ConfigText = @'
[analytics]
enabled = false

[telemetry]
enabled = false

[traces]
enabled = false

[server]
host = "127.0.0.1"

[agent]
tools = ""
context_from_memory = false

[tools]
enabled = []

[tools.mcp]
enabled = false

[memory]
enabled = false

[channel]
enabled = false

[learning]
enabled = false
auto_update = false
training_enabled = false

[proactive]
enabled = false

[scheduler]
enabled = false

[workflow]
enabled = false

[sessions]
enabled = false

[a2a]
enabled = false

[operators]
enabled = false
auto_activate = ""

[security]
enabled = true
mode = "block"
enforce_tool_confirmation = true
local_engine_bypass = false
local_tool_bypass = false

[security.capabilities]
enabled = false
'@

$SecretEnvironmentNames = @(
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "MISTRAL_API_KEY",
    "GROQ_API_KEY",
    "COHERE_API_KEY",
    "HUGGINGFACE_TOKEN",
    "HF_TOKEN",
    "GITHUB_TOKEN"
)
$savedSecrets = Save-ProcessEnvironment $SecretEnvironmentNames
$candidateResults = @()
$allPassed = $true

try {
    foreach ($name in $SecretEnvironmentNames) {
        [Environment]::SetEnvironmentVariable($name, $null, "Process")
    }

    foreach ($candidate in @($pin.candidates)) {
        $startedAt = (Get-Date).ToUniversalTime().ToString("o")
        $slug = [regex]::Replace([string]$candidate.name, "[^A-Za-z0-9._-]", "-")
        $expectedSha = [string]$candidate.resolved_commit_sha
        if ($expectedSha -notmatch "^[0-9a-f]{40}$") {
            throw "Candidate '$slug' does not have an exact commit SHA."
        }

        $candidateRoot = Join-Path (Join-Path $OutputRoot "candidates") $slug
        $sourceDir = Join-Path $candidateRoot "source"
        $runtimeHome = Join-Path $candidateRoot "runtime-home"
        $candidateRunRoot = Join-Path $RunRoot $slug
        New-Item -ItemType Directory -Path $candidateRoot -Force | Out-Null
        New-Item -ItemType Directory -Path $runtimeHome -Force | Out-Null
        New-Item -ItemType Directory -Path $candidateRunRoot -Force | Out-Null

        $result = [ordered]@{
            name = [string]$candidate.name
            expected_sha = $expectedSha
            head_sha = $null
            source_assessment_passed = $false
            dependency_sync_passed = $false
            import_passed = $false
            config_checks_passed = $false
            package_version = $null
            module_relative_path = $null
            started_at_utc = $startedAt
            completed_at_utc = $null
            status = "failed"
            error = $null
        }

        Write-Host "Evaluating exact candidate: $($candidate.name)"
        try {
            if (-not (Test-Path $sourceDir)) {
                New-Item -ItemType Directory -Path $sourceDir | Out-Null
                Invoke-LoggedCommand -FilePath $Git -Arguments @("init", "--quiet", $sourceDir) `
                    -WorkingDirectory $RepoRoot -LogPath (Join-Path $candidateRunRoot "git-init.log") | Out-Null
                Invoke-LoggedCommand -FilePath $Git -Arguments @("-C", $sourceDir, "remote", "add", "origin", [string]$pin.upstream) `
                    -WorkingDirectory $RepoRoot -LogPath (Join-Path $candidateRunRoot "git-remote.log") | Out-Null
                Invoke-LoggedCommand -FilePath $Git -Arguments @("-C", $sourceDir, "fetch", "--depth", "1", "origin", $expectedSha) `
                    -WorkingDirectory $RepoRoot -LogPath (Join-Path $candidateRunRoot "git-fetch.log") | Out-Null
                Invoke-LoggedCommand -FilePath $Git -Arguments @("-C", $sourceDir, "checkout", "--detach", "FETCH_HEAD") `
                    -WorkingDirectory $RepoRoot -LogPath (Join-Path $candidateRunRoot "git-checkout.log") | Out-Null
            }
            elseif (-not (Test-Path (Join-Path $sourceDir ".git"))) {
                throw "Existing candidate source directory is not a Git checkout; it was left untouched."
            }

            $headSha = (& $Git -C $sourceDir rev-parse HEAD).ToString().Trim()
            if ($LASTEXITCODE -ne 0 -or $headSha -ne $expectedSha) {
                throw "Existing candidate checkout does not match its exact approved commit; it was left untouched."
            }
            $dirty = (& $Git -C $sourceDir status --porcelain --untracked-files=all)
            if ($LASTEXITCODE -ne 0 -or $dirty) {
                throw "Existing candidate checkout is not clean; it was left untouched."
            }
            $result.head_sha = $headSha

            $sourceReportPath = Join-Path $candidateRunRoot "source-assessment.json"
            Invoke-LoggedCommand -FilePath $Python `
                -Arguments @($AssessorPath, "--source", $sourceDir, "--expected-sha", $expectedSha, "--output", $sourceReportPath) `
                -WorkingDirectory $RepoRoot -LogPath (Join-Path $candidateRunRoot "source-assessment.log") | Out-Null
            $sourceReport = Get-Content -Path $sourceReportPath -Raw | ConvertFrom-Json
            if (-not $sourceReport.passed) {
                throw "Source identity assessment did not pass."
            }
            $result.source_assessment_passed = $true

            $RuntimeEnvironmentNames = @(
                "OPENJARVIS_HOME",
                "OPENJARVIS_CONFIG",
                "USERPROFILE",
                "DO_NOT_TRACK",
                "PYTHONNOUSERSITE",
                "UV_CACHE_DIR",
                "UV_NO_PROGRESS"
            )
            $savedRuntimeEnvironment = Save-ProcessEnvironment $RuntimeEnvironmentNames
            try {
                $configPath = Join-Path $runtimeHome "config.toml"
                [System.IO.File]::WriteAllText($configPath, $ConfigText, $Utf8NoBom)
                [Environment]::SetEnvironmentVariable("OPENJARVIS_HOME", $runtimeHome, "Process")
                [Environment]::SetEnvironmentVariable("OPENJARVIS_CONFIG", $configPath, "Process")
                [Environment]::SetEnvironmentVariable("USERPROFILE", $runtimeHome, "Process")
                [Environment]::SetEnvironmentVariable("DO_NOT_TRACK", "1", "Process")
                [Environment]::SetEnvironmentVariable("PYTHONNOUSERSITE", "1", "Process")
                [Environment]::SetEnvironmentVariable("UV_CACHE_DIR", (Join-Path $OutputRoot "uv-cache"), "Process")
                [Environment]::SetEnvironmentVariable("UV_NO_PROGRESS", "1", "Process")

                Invoke-LoggedCommand -FilePath $Uv -Arguments @("sync", "--frozen", "--no-dev") `
                    -WorkingDirectory $sourceDir -LogPath (Join-Path $candidateRunRoot "uv-sync.log") | Out-Null
                $result.dependency_sync_passed = $true

                $importCode = @'
import importlib.metadata as metadata
import json
import pathlib
import sys

import openjarvis
from openjarvis.core.config import load_config

root = pathlib.Path(sys.argv[1]).resolve()
module = pathlib.Path(openjarvis.__file__).resolve()
within = root == module or root in module.parents
config = load_config()
checks = {
    "analytics_disabled": not config.analytics.enabled,
    "telemetry_disabled": not config.telemetry.enabled,
    "loopback_only": config.server.host == "127.0.0.1",
    "tools_empty": not config.tools.enabled,
    "mcp_disabled": not config.tools.mcp.enabled,
    "memory_context_disabled": not config.agent.context_from_memory,
    "channels_disabled": not config.channel.enabled,
    "learning_disabled": not config.learning.enabled,
    "security_enabled": config.security.enabled,
    "security_blocks": config.security.mode == "block",
    "engine_bypass_disabled": not config.security.local_engine_bypass,
    "tool_bypass_disabled": not config.security.local_tool_bypass,
}
report = {
    "version": metadata.version("openjarvis"),
    "module_within_source": within,
    "module_relative_path": module.relative_to(root).as_posix() if within else None,
    "config_checks": checks,
    "config_checks_passed": all(checks.values()),
}
print(json.dumps(report, sort_keys=True))
sys.exit(0 if within and report["config_checks_passed"] else 1)
'@
                $importOutput = @(Invoke-LoggedCommand -FilePath $Uv `
                    -Arguments @("run", "--frozen", "--no-sync", "python", "-c", $importCode, $sourceDir) `
                    -WorkingDirectory $sourceDir -LogPath (Join-Path $candidateRunRoot "import.log"))
                $importReport = $importOutput[-1] | ConvertFrom-Json
                if (-not $importReport.module_within_source) {
                    throw "Imported package did not come from the exact candidate checkout."
                }
                $result.import_passed = $true
                $result.config_checks_passed = [bool]$importReport.config_checks_passed
                $result.package_version = [string]$importReport.version
                $result.module_relative_path = [string]$importReport.module_relative_path
            }
            finally {
                Restore-ProcessEnvironment $savedRuntimeEnvironment
            }

            $finalHead = (& $Git -C $sourceDir rev-parse HEAD).ToString().Trim()
            $finalDirty = (& $Git -C $sourceDir status --porcelain --untracked-files=all)
            if ($LASTEXITCODE -ne 0 -or $finalHead -ne $expectedSha -or $finalDirty) {
                throw "Candidate source identity or cleanliness changed during evaluation."
            }

            $result.status = "passed"
            Write-Host "PASS: source, dependency sync and import checks completed for $($candidate.name)."
        }
        catch {
            $allPassed = $false
            $result.error = $_.Exception.Message
            Write-Warning "Candidate $($candidate.name) failed: $($result.error)"
        }
        finally {
            $result.completed_at_utc = (Get-Date).ToUniversalTime().ToString("o")
            $candidateResults += [pscustomobject]$result
        }
    }
}
finally {
    Restore-ProcessEnvironment $savedSecrets
}

$summary = [ordered]@{
    schema_version = "1.0"
    run_id = $RunId
    phase = 0
    scope = "Exact source, dependency sync, import and fail-closed config checks only; no model, tool, connector or server was invoked."
    python_version = $pythonVersionText
    candidates = $candidateResults
    passed = $allPassed
}
$summaryPath = Join-Path $RunRoot "summary.json"
Write-JsonNoBom -Value $summary -Path $summaryPath

if (-not $allPassed) {
    throw "One or more candidates failed. Review the private local summary: $summaryPath"
}

Write-Host "PASS: both exact OpenJarvis candidates completed the controlled import evaluation."
Write-Host "Private local evidence: $summaryPath"
Write-Host "Phase 1 remains blocked; this result does not select an OpenJarvis baseline."
