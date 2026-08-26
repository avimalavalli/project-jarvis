# Avi's PC Assessment Runbook

Phase 0 runtime and hardware claims require evidence from Avi's existing PC.
The cloud engineering workspace is not a substitute.

## Safe inventory

From PowerShell in a local clone:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
./scripts/windows/collect_pc_inventory.ps1
```

The script writes `artifacts/phase0/pc-inventory.json`. The `artifacts/`
directory is ignored by Git. Inspect the JSON before sharing it. It intentionally
does not collect user name, hostname, serial numbers, environment variables,
network addresses, files or credentials.

## What the evidence decides

- Supported OpenJarvis/Python installation path.
- Whether local inference is viable and which model sizes to benchmark.
- Whether container isolation is available.
- Audio-device baseline for the later voice phase.
- Whether any targeted RAM, SSD, GPU or audio upgrade is justified.

No hardware purchase is recommended from inventory alone. Workload latency,
memory use, thermals and reliability must be measured first.

