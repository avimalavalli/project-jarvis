[CmdletBinding()]
param(
    [string]$OutputPath = "artifacts/phase0/pc-inventory.json"
)

$ErrorActionPreference = "Stop"

function Get-CommandVersion {
    param([Parameter(Mandatory = $true)][string]$Name)
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $command) {
        return $null
    }
    try {
        $firstLine = (& $Name --version 2>&1 | Select-Object -First 1).ToString()
        return $firstLine
    }
    catch {
        return "present; version unavailable"
    }
}

$os = Get-CimInstance Win32_OperatingSystem
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$gpus = Get-CimInstance Win32_VideoController | ForEach-Object {
    [ordered]@{
        name = $_.Name
        adapter_ram_bytes = if ($null -eq $_.AdapterRAM) { $null } else { [int64]$_.AdapterRAM }
        driver_version = $_.DriverVersion
    }
}
$disks = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    [ordered]@{
        drive = $_.DeviceID
        size_bytes = [int64]$_.Size
        free_bytes = [int64]$_.FreeSpace
    }
}
$audio = Get-CimInstance Win32_SoundDevice | ForEach-Object {
    [ordered]@{ name = $_.Name; status = $_.Status }
}

$inventory = [ordered]@{
    schema_version = "1.0"
    collected_at_utc = (Get-Date).ToUniversalTime().ToString("o")
    privacy_note = "No user name, hostname, serial number, network address, environment variable, file listing or credential is collected."
    os = [ordered]@{
        caption = $os.Caption
        version = $os.Version
        build_number = $os.BuildNumber
        architecture = $os.OSArchitecture
    }
    cpu = [ordered]@{
        name = $cpu.Name
        physical_cores = $cpu.NumberOfCores
        logical_processors = $cpu.NumberOfLogicalProcessors
        max_clock_mhz = $cpu.MaxClockSpeed
    }
    memory = [ordered]@{
        total_bytes = [int64]$os.TotalVisibleMemorySize * 1KB
        free_bytes = [int64]$os.FreePhysicalMemory * 1KB
    }
    gpu = @($gpus)
    fixed_disks = @($disks)
    audio = @($audio)
    powershell_version = $PSVersionTable.PSVersion.ToString()
    tools = [ordered]@{
        git = Get-CommandVersion "git"
        python = Get-CommandVersion "python"
        uv = Get-CommandVersion "uv"
        node = Get-CommandVersion "node"
        docker = Get-CommandVersion "docker"
        podman = Get-CommandVersion "podman"
        ollama = Get-CommandVersion "ollama"
        nvidia_smi = Get-CommandVersion "nvidia-smi"
    }
}

$resolved = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputPath))
$parent = Split-Path -Parent $resolved
New-Item -ItemType Directory -Path $parent -Force | Out-Null
$inventory | ConvertTo-Json -Depth 6 | Set-Content -Path $resolved -Encoding UTF8
Write-Host "Inventory written to $resolved"

