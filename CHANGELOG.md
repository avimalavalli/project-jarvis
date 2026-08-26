# Changelog

All notable Project JARVIS changes are recorded here.

## [Unreleased]

### Added

- Phase 0 public-safe repository scaffold.
- Blueprint fingerprint and doctrine record.
- Draft architecture, threat model, data classification, ADR and risk register.
- Draft action, audit, device, memory, model-route and tool-capability contracts.
- Zero-capability OpenJarvis evaluation policy.
- Local and CI foundation validation.
- ADR-0002 defining the public-source/private-data boundary.
- Phase 0 persona, permissions, memory, routing, device and ownership specifications.
- Event contract, golden evaluation skeleton and fail-closed environment profiles.
- Backup/recovery and actual-PC assessment runbooks.
- Safe Windows hardware inventory and OpenJarvis source-identity assessment scripts.
- Exact stable and newer OpenJarvis candidate commits.
- Preliminary keyless sandbox installation and import evidence for both exact candidates.
- SHA-pinned GitHub Actions and repository-wide CODEOWNERS.
- Enforced `main` branch protection requiring pull requests and the `foundation` CI check.
- ADR-0003 defining laptop development, larger-PC testing and single-identity Core migration.
- Fail-closed Windows harness for exact OpenJarvis source, dependency and import checks.
- Privacy-safe laptop inventory assessment without committing the private raw report.

### Security

- Default-deny tools, loopback-only networking, no-cloud evaluation and
  external-telemetry-off assertions.
- Windows candidate evaluation clears common provider credentials, isolates
  runtime state, and refuses administrator execution or automatic setup.

### Fixed

- Windows PowerShell 5.1 version probes now validate captured output directly
  instead of relying on native exit-state propagation through a pipeline.
- Recorded recovery from a delayed Phase 0 pull-request check during Windows evaluation.
