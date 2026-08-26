# OpenJarvis Candidate Evaluation

Status: Preliminary sandbox installation evidence captured; runtime selection
remains open.

## Immutable candidates

| Candidate | Exact commit | Purpose |
|---|---|---|
| Stable `v1.0.2` | `56c9a59f8dfa138f16afd3ccff5d394a13801162` | Packaged stable baseline |
| Newer candidate | `dbd4a1dfd75e9ce12aa21ea99a9970cb4eb47074` | Newer security/platform line without the following traffic-only commit |

## Verified source-only evidence — 2026-08-26

- Both checkouts resolved to the expected immutable SHA and had clean trees.
- Neither checkout was imported or executed during this inspection.
- Stable declares Python `>=3.10`; newer declares `>=3.10,<3.14`.
- Both contain the engine, security and tools packages.
- The newer candidate has a top-level `memory` package; stable `v1.0.2` does
  not. This is a capability/layout finding, not proof that either memory design
  meets JARVIS requirements.
- Stable tracks 1,949 files and 547 Python test files; newer tracks 2,108 files
  and 614 Python test files.
- The candidate delta is large: 681 files changed, 72,204 insertions and 12,804
  deletions. Runtime selection therefore cannot be inferred from release age.

Source reports were written to ignored local `artifacts/phase0/` files.

## Verified preliminary sandbox evidence — 2026-08-26

- Each exact candidate was installed independently with `uv sync --frozen
  --no-dev` into its own project-local virtual environment.
- No API key, model, tool, connector or server was configured or invoked.
- Stable installed as `openjarvis==1.0.2` and imported from the expected
  `src/openjarvis` checkout at commit
  `56c9a59f8dfa138f16afd3ccff5d394a13801162`.
- Newer installed as `openjarvis==0.0.1.dev1+unknown.gdbd4a1dfd` and imported
  from the expected `src/openjarvis` checkout at commit
  `dbd4a1dfd75e9ce12aa21ea99a9970cb4eb47074`.
- Both upstream worktrees remained clean after the checks.

This evidence proves dependency resolution, package build and import only in an
isolated Linux sandbox. It does **not** prove Windows support, runtime safety,
model inference, network behaviour, credential handling, tool isolation or
performance on Avi's computer. No candidate is selected.

## Evaluation stages

1. **Source identity:** exact SHA, clean tree, Python requirement, expected
   subsystem layout and zero JARVIS patches.
2. **Isolated install:** repeat the verified sandbox install in a fresh
   environment on Avi's PC; capture resolver, package and doctor output.
3. **Zero-capability configuration:** loopback only, external analytics off,
   no cloud keys, tools, connectors or automatic memory.
4. **Runtime tests:** upstream tests, doctor, strict boundary scan and one local
   zero-key inference smoke test.
5. **Security observation:** listeners, egress, files created, credential
   persistence, logs and failure behaviour.
6. **Performance:** cold/warm latency, tokens per second, RAM/VRAM, CPU/GPU,
   thermals and idle cost on Avi's PC.
7. **Decision:** compare reproducibility, security, Windows support, patch
   burden and performance; accept one exact SHA in ADR-0001.

## Prohibited shortcuts

- No floating `main` dependency.
- No one-line installer before its actions are reviewed.
- No credential entered during the zero-key evaluation.
- No unsandboxed tool execution because a container runtime is absent.
- No claim that source inspection proves runtime safety.
