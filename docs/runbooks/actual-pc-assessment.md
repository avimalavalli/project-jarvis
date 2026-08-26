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

## Controlled candidate install/import

This step is run only after the inventory has been reviewed. Open a normal
PowerShell window, not an administrator window, from the repository folder:

```powershell
./scripts/windows/evaluate_openjarvis_candidates.ps1
```

The harness needs Git, Python 3.10–3.13 and `uv` to already be installed. It
will stop with a clear message if a prerequisite or 10 GiB of free space is
missing. It does not install missing programs.

The harness checks out both approved commits into ignored `artifacts/` storage,
uses separate virtual environments and private runtime homes, disables
analytics and capabilities, and performs source, dependency and import checks
plus verifies that upstream loaded the safety settings. It does not start
JARVIS, a model, a server, a connector or a tool.

Successful output identifies a private local `summary.json`. Inspect that file
before sharing it. A successful run is evidence for Windows install/import only;
it neither selects an OpenJarvis baseline nor authorises Phase 1.

## What the evidence decides

- Supported OpenJarvis/Python installation path.
- Whether local inference is viable and which model sizes to benchmark.
- Whether container isolation is available.
- Audio-device baseline for the later voice phase.
- Whether any targeted RAM, SSD, GPU or audio upgrade is justified.

No hardware purchase is recommended from inventory alone. Workload latency,
memory use, thermals and reliability must be measured first.

Development occurs on the laptop. The larger PC repeats compatibility and
performance tests against the same reviewed commit. Private identity and
canonical state remain single-authority data and are not copied through Git;
ADR-0003 controls any future Core migration.
